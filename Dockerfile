# 使用するベースイメージ
FROM python:3.11-slim

# 環境変数を設定して、Pythonがバッファリングされないようにする
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリをインストール
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    imagemagick \
    libmagic1 \
    # ghostscript \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# policy.xml ファイルの該当の行をコメントアウト
RUN sed -i 's|<policy domain="path" rights="none" pattern="@\*"/>|<!-- <policy domain="path" rights="none" pattern="@*"/> -->|' /etc/ImageMagick-6/policy.xml

RUN pip install pipenv

# PipfileとPipfile.lockをコピー
COPY Pipfile* /app/

# Pythonの依存関係をインストール
RUN pipenv install --system --deploy

# 必要なファイルをコピー
COPY main.py create_video_post.py test.py /app/
COPY fonts/LINESeedJP_A_TTF_Bd.ttf /app/fonts/


# アプリケーションを実行
CMD ["python", "main.py"]
