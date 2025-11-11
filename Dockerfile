ARG python_image_v="python:3.12-slim"
# python3.13のイメージをダウンロード
FROM ${python_image_v}

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    git \
    cmake \
    ffmpeg \
    python3-pip \
    zip \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -U pip

RUN echo "/app/python_modules/python/lib/python3.12/site-packages/" > /usr/local/lib/python3.12/site-packages/.pth

# poetryのインストール先の指定
ENV POETRY_VERSION=2.2.0 \
    POETRY_HOME=/opt/poetry

# poetryインストール
RUN curl -sSL https://install.python-poetry.org/ | python - --version ${POETRY_VERSION} && \
    # シンボリックによるpathへのpoetryコマンドの追加
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    # 仮想環境を作成しない設定(コンテナ前提のため，仮想環境を作らない)
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry self add poetry-plugin-export && \
    poetry self update

# Copy application code
COPY . /app

WORKDIR /app

# Run the application
CMD ["poetry", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]
