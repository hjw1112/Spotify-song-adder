FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TESSERACT_CMD=/usr/bin/tesseract
RUN echo "export TESSERACT_CMD=/usr/bin/tesseract" >> ~/.bashrc

EXPOSE $PORT

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
