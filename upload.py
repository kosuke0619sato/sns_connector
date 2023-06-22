import google.cloud.storage as gcs
import requests

imageURL = "https://thumb.photo-ac.com/15/1537ecd123466274baaee7c19a95f8ca_w.jpeg"

accessToken = "EAAOBjQTg4vgBAEQGfGktYhvi8BfjnccZBctK5VEf6ZCDx6t2lHNwKHpRSqZCymnt9Ingcm23TNXPp7Dx65hGhc9mxLBcQ18RohOvhQynrcWFFmGUz0XgZCFG3cgh82zQTB5dmqIwJ5h9cHuFRiR752Md7uTIySll4XRUnEZAcQb27g5eehYFUWBERyVt4iukfMyx3hsSZCMqEcD73VRII309KmsvFZC008hokyc75kgAnCbmwZCHaZAJQJt7PmMcfMZAcZD"
IG_USER_ID = "17841460386043830"
# url = f"https://graph.facebook.com/v17.0/{IG_USER_ID}/media?access_token={accessToken}"

# publish_response = requests.get(url).json()
# print(publish_response)

# # Google Cloud Storageから動画をダウンロード
# # storage_client = gcs.Client()
# # bucket = storage_client.get_bucket('your-bucket-name')
# # blob = bucket.get_blob('path/to/your/video.mp4')
# # video_content = blob.download_as_string()

videoURL = ".\outputs\output.mp4"

# 動画をアップロードする
upload_url = "https://graph.facebook.com/v17.0/{}/media".format(IG_USER_ID)
files = {"video": open(videoURL, "rb")}
upload_payload = {
    "media_type": "VIDEO",
    # "video_url": videoURL,
    "caption": "sample caption here",
    "access_token": accessToken,
}
# files = {"video": open(videoURL, "rb")}

upload_response = requests.post(upload_url, files=files, data=upload_payload)
# upload_response = requests.post(upload_url, files=files, data=upload_payload)
# upload_response = requests.post(upload_url, files={'video': ('video.mp4', video_content)}, data=upload_payload)

# アップロードされた動画を投稿する
# media_id = upload_response.json()
media_id = upload_response.json().get("id")

publish_url = f"https://graph.facebook.com/v17.0/{media_id}/media_publish"
publish_payload = {"access_token": accessToken}
publish_response = requests.post(publish_url, data=publish_payload)

print(publish_response.json())
