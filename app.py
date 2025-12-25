"""
LiteLLM Tabanlı Micro-SaaS API
Flask ile hafif ve hızlı bir LLM API servisi
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from litellm import completion

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask uygulaması oluştur
app = Flask(__name__)

# CORS ayarları - tüm domainlere izin ver (geliştirme için)
CORS(app)

# Ortam değişkenlerinden API key'leri al
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# API key kontrolü
if not ANTHROPIC_API_KEY and not OPENAI_API_KEY:
    logger.warning("Uyarı: ANTHROPIC_API_KEY veya OPENAI_API_KEY ortam değişkeni tanımlı değil!")


@app.route('/health', methods=['GET'])
def health_check():
    """
    Sağlık kontrolü endpoint'i
    """
    return jsonify({
        'status': 'healthy',
        'service': 'LiteLLM API'
    }), 200


@app.route('/ask', methods=['POST'])
def ask():
    """
    LLM'e soru sorma endpoint'i
    
    Request Body:
        {
            "prompt": "Kullanıcının sorusu",
            "model": "claude-3-5-sonnet" (opsiyonel)
        }
    
    Returns:
        JSON response with LLM answer
    """
    try:
        # Request body'yi al
        data = request.get_json()
        
        # Validasyon
        if not data:
            return jsonify({
                'error': 'Request body boş olamaz',
                'message': 'JSON formatında prompt gönderilmelidir'
            }), 400
        
        if 'prompt' not in data:
            return jsonify({
                'error': 'Prompt parametresi eksik',
                'message': 'Request body içinde "prompt" alanı zorunludur'
            }), 400
        
        prompt = data.get('prompt')
        model = data.get('model', 'claude-3-5-sonnet')  # Varsayılan model
        
        if not prompt or not prompt.strip():
            return jsonify({
                'error': 'Prompt boş olamaz',
                'message': 'Prompt alanı dolu olmalıdır'
            }), 400
        
        logger.info(f"İstek alındı - Model: {model}, Prompt uzunluğu: {len(prompt)}")
        
        # LiteLLM ile completion çağrısı
        response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Response'dan cevabı çıkar
        answer = response.choices[0].message.content
        
        logger.info(f"Başarılı yanıt - Model: {model}")
        
        return jsonify({
            'success': True,
            'model': model,
            'answer': answer,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens if hasattr(response.usage, 'prompt_tokens') else None,
                'completion_tokens': response.usage.completion_tokens if hasattr(response.usage, 'completion_tokens') else None,
                'total_tokens': response.usage.total_tokens if hasattr(response.usage, 'total_tokens') else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"API hatası: {str(e)}", exc_info=True)
        
        # LiteLLM'e özgü hata mesajları
        error_message = str(e)
        
        if 'api_key' in error_message.lower() or 'authentication' in error_message.lower():
            return jsonify({
                'error': 'API Key hatası',
                'message': 'Geçersiz veya eksik API anahtarı. Lütfen ortam değişkenlerini kontrol edin.'
            }), 401
        
        if 'rate limit' in error_message.lower() or 'quota' in error_message.lower():
            return jsonify({
                'error': 'Rate limit aşıldı',
                'message': 'API kullanım limiti aşıldı. Lütfen daha sonra tekrar deneyin.'
            }), 429
        
        if 'model' in error_message.lower() and 'not found' in error_message.lower():
            return jsonify({
                'error': 'Model bulunamadı',
                'message': f'Belirtilen model ({model if "model" in locals() else "bilinmiyor"}) bulunamadı veya erişilemiyor.'
            }), 400
        
        # Genel hata
        return jsonify({
            'error': 'İç sunucu hatası',
            'message': 'LLM servisi ile iletişim kurulurken bir hata oluştu.',
            'details': error_message
        }), 500


@app.errorhandler(404)
def not_found(error):
    """
    404 hata yöneticisi
    """
    return jsonify({
        'error': 'Endpoint bulunamadı',
        'message': 'İstenen endpoint mevcut değil. Lütfen /ask veya /health endpoint\'lerini kullanın.'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    405 hata yöneticisi
    """
    return jsonify({
        'error': 'Method not allowed',
        'message': 'Bu endpoint için izin verilmeyen HTTP metodu kullanıldı.'
    }), 405


if __name__ == '__main__':
    # Development modu için
    app.run(host='0.0.0.0', port=5000, debug=False)
else:
    # Production modu (gunicorn ile çalışırken)
    logger.info("Uygulama gunicorn ile başlatılıyor...")

