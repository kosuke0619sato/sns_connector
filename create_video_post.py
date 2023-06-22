import logging
import os
import shutil
import tempfile

from google.cloud import storage
from moviepy.config import change_settings
from moviepy.editor import TextClip, concatenate_videoclips

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
# local 環境
# change_settings(
#     {"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"}
# )

# 標準 Logger の設定
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s", level=logging.DEBUG
)
logger = logging.getLogger()


# TikTokのショート動画のサイズ
CW, CH = 1080, 1920  # 幅と高さ

text_duration = 4
title_duration = 2

GCP_PROJECT_ID = "storied-groove-389314"
GCS_BUCKET_NAME = "auto_generated_videos"


def upload_to_gcs(file_path, bucket_name, dest_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(dest_blob_name)
        blob.upload_from_filename(file_path)
    except Exception as e:
        logger.error(f"Error uploading video file: {e}")
        raise
    else:
        return f"https://storage.googleapis.com/{bucket_name}/{dest_blob_name}"


def generateFinalClip(title, texts):
    clips = []
    try:
        title_width = CW * 0.8
        title_fontSize = title_width / 8 if len(title) < 24 else title_width / 12
        title_clip = createTextClip(
            title, title_width, title_fontSize, text_duration, False
        )
        clips.append(title_clip)
        text_width = CW * 0.8
        text_fontSize = (
            text_width / 8 if all(len(text) < 24 for text in texts) else text_width / 12
        )
        for text in texts:
            text_clip = createTextClip(
                text, text_width, text_fontSize, title_duration, True
            )
            clips.append(text_clip)
        final_clip = concatenate_videoclips(clips, method="chain")
    except Exception as e:
        # write_videofileメソッドでエラーが発生した場合、ここで処理します
        logger.error(f"Error generating final clip: {e}")
    else:
        return final_clip


def createTextClip(text, width, fontSize, duration, fadeEffect):
    strokeWidth = fontSize / 20
    position = "center"
    fadeInDuration = 0.5
    fadeoutDuration = 0.2
    font = r"./fonts/LINESeedJP_A_TTF_Bd.ttf"
    textWithStroke = (
        TextClip(
            txt=text,
            font=font,
            fontsize=fontSize,
            color="white",
            method="caption",
            size=[width, None],  # Set the size of the text box
            stroke_width=strokeWidth,
            stroke_color="black",
        )
        .set_position(("center", position))
        .set_duration(duration)
        .on_color(size=(CW, CH), color=(0, 0, 0), col_opacity=0)
    )

    return (
        textWithStroke.fadein(fadeInDuration).fadeout(fadeoutDuration)
        if fadeEffect
        else textWithStroke.fadeout(fadeoutDuration)
    )


def create_video_post(title, texts):
    output_dir = None
    try:
        final_clip = generateFinalClip(title, texts)
        output_dir = tempfile.mkdtemp()
        fileName = f"{title}.mp4"
        output_file_path = os.path.join(output_dir, fileName)
        final_clip.write_videofile(output_file_path, fps=24, codec="libx264")
    except Exception as e:
        # write_videofileメソッドでエラーが発生した場合、ここで処理します
        logger.error(f"Error saving video file: {e}")
        return None

    video_url = upload_to_gcs(output_file_path, GCS_BUCKET_NAME, fileName)
    if output_dir:
        shutil.rmtree(output_dir)
    if video_url is None:
        logger.error("Failed to upload video")
        return None

    return video_url
