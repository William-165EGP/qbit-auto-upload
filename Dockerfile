FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
  ca-certificates \
  curl \
  unzip \
&& curl https://rclone.org/install.sh | bash \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY auto_upload.py .

CMD ["python", "auto_upload.py"] 
