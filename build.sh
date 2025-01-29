set -o errexit 

apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

pip install --no-cache-dir -r requirements.txt
