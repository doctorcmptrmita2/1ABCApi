# LiteLLM Micro-SaaS API

Flask ve LiteLLM kullanarak oluşturulmuş, Dockerize edilmiş bir Micro-SaaS API projesi. Easypanel üzerinde kolayca deploy edilebilir.

## 🚀 Özellikler

- **Flask Framework**: Hafif ve hızlı web framework
- **LiteLLM Entegrasyonu**: Çoklu LLM provider desteği (Anthropic, OpenAI, vb.)
- **Docker Support**: Production-ready container yapılandırması
- **Easypanel Uyumlu**: Port 80 üzerinden otomatik algılama
- **CORS Desteği**: Tüm domainlerden erişim (geliştirme için)
- **Hata Yönetimi**: Kapsamlı hata yakalama ve loglama

## 📋 Gereksinimler

- Docker ve Docker Compose
- Easypanel hesabı (veya benzer container platform)
- Anthropic veya OpenAI API key

## 🛠️ Kurulum

### 1. Projeyi Klonlayın

```bash
git clone <repo-url>
cd 1ABCApi
```

### 2. Ortam Değişkenlerini Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın ve API key'lerinizi ekleyin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

### 3. Docker ile Çalıştırma

#### Yerel Geliştirme

```bash
docker build -t litellm-api .
docker run -p 80:80 --env-file .env litellm-api
```

#### Production (Easypanel)

1. Easypanel dashboard'a giriş yapın
2. Yeni bir proje oluşturun
3. Docker image'ı deploy edin
4. Ortam değişkenlerini `.env` dosyasından ekleyin
5. Port 80'i otomatik algılaması için bırakın

## 📡 API Kullanımı

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "LiteLLM API"
}
```

### Ask Endpoint

```bash
POST /ask
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "Python'da liste nasıl oluşturulur?",
  "model": "claude-3-5-sonnet"
}
```

**Response (Success):**
```json
{
  "success": true,
  "model": "claude-3-5-sonnet",
  "answer": "Python'da liste oluşturmak için...",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

**Response (Error):**
```json
{
  "error": "API Key hatası",
  "message": "Geçersiz veya eksik API anahtarı..."
}
```

## 🔧 Yapılandırma

### Desteklenen Modeller

- `claude-3-5-sonnet` (varsayılan)
- `claude-3-opus`
- `claude-3-sonnet`
- `gpt-4`
- `gpt-3.5-turbo`
- Ve diğer LiteLLM destekli modeller

### Ortam Değişkenleri

| Değişken | Açıklama | Zorunlu |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API anahtarı | Claude için |
| `OPENAI_API_KEY` | OpenAI API anahtarı | OpenAI için |

## 🐳 Docker Detayları

- **Base Image**: `python:3.9-slim`
- **Port**: 80
- **Workers**: 2 (gunicorn)
- **Timeout**: 120 saniye

## 📝 Geliştirme

### Yerel Geliştirme (Docker olmadan)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python app.py
```

### Loglama

Uygulama `logging` modülü kullanarak loglama yapar. Loglar stdout'a yazılır ve Docker loglarından görüntülenebilir.

## 🔒 Güvenlik

- API key'ler asla kod içinde hardcoded değildir
- Ortam değişkenleri üzerinden güvenli şekilde yönetilir
- Production'da CORS ayarlarını kısıtlamayı düşünün

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için önce bir issue açarak neyi değiştirmek istediğinizi tartışın.

