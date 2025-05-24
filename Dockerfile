FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV POKEMON_DATASET_PATH=/app/pokemon_dataset

# 1. Install base packages, X11 client libraries, and unzip
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    unzip \
    x11-xserver-utils libx11-6 libxcursor1 libxrandr2 libxss1 libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Add the Deadsnakes PPA and install Python 3.12 + dev + venv
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-dev python3.12-venv fontconfig \
    && apt-get clean && rm -rf /var/lib/apt/lists/* 

# 3. Install pip for Python 3.12
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# 4. Install Poetry, setuptools, wheel, and Kaggle CLI
RUN pip3.12 install --no-cache-dir poetry setuptools wheel kaggle

# 5. Set work directory and copy project files
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

# Create pokemon dataset directory
RUN mkdir -p ${POKEMON_DATASET_PATH} && chmod 777 ${POKEMON_DATASET_PATH}

# Copy project scripts explicitly
COPY bubble_game.py /app/
COPY pokemon_kaggle_download.py /app/
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# 6. Default to a shell (override at runtime to run your game)
CMD ["/bin/bash"]
