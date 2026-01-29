FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpipewire-0.3-0 \
    libpulse0 \
    pulseaudio-utils \
    libportaudio2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
