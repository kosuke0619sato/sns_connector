import json
import logging
import os

from flask import Flask, jsonify, request

from create_video_post import create_video_post

app = Flask(__name__)

# 標準 Logger の設定
logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s", level=logging.DEBUG
)
logger = logging.getLogger()


@app.route("/", methods=["POST"])
def main_entry():
    # リクエストの JSON ボディを取得
    request_json = request.get_json(silent=True)

    # リクエストに JSON データが含まれている場合
    if request_json:
        logger.info(f"Received data: {json.dumps(request_json)}")

        # 必要なフィールドをチェックする
        required_fields = ["title", "text1", "text2", "text3", "text4", "text5"]
        missing_fields = [
            field for field in required_fields if field not in request_json
        ]

        # 必要なフィールドが欠けている場合はエラーを返す
        if missing_fields:
            return (
                jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}),
                400,
            )

        # create_video_post関数にJSONデータをキーワード引数として渡す
        texts = [request_json.get(f"text{i}") for i in range(1, 6)]
        stored_url = create_video_post(request_json.get("title"), texts)

        if stored_url:
            return jsonify({"url": stored_url}), 200
        else:
            return jsonify({"error": "Video generation failed."}), 500
    else:
        return jsonify({"error": "Invalid request: JSON data expected."}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
