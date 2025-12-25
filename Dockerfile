# Python 3.9 slim base image kullan (küçük boyut için)
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem paketlerini güncelle ve gerekli paketleri kur
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY app.py .

# Port 80'i expose et (Easypanel otomatik algılama için)
EXPOSE 80

# Gunicorn ile uygulamayı başlat
# Worker sayısı: 2, Bind: 0.0.0.0:80, Timeout: 120 saniye
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

