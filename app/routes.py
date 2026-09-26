"""İstek doğrulama ve yönlendirme; SQL veya AI sağlayıcı kodu içermez."""
import hmac
import re
from datetime import datetime
from flask import Blueprint, current_app, jsonify, render_template, request
from . import database
from .services.ai_service import ai_service, AIServiceError

pages = Blueprint('pages', __name__)
api = Blueprint('api', __name__)

@pages.context_processor
def common_template_data():
    return {'current_year': datetime.now().year}

@pages.get('/koleksiyon')
def collection():
    return render_template('collection.html')

@pages.get('/hakkimizda')
def about():
    return render_template('about.html')

@pages.get('/iletisim')
def contact():
    return render_template('contact.html')

@pages.get('/gizlilik')
def privacy():
    return render_template('privacy.html')

def hata(mesaj, status=400):
    return jsonify(basari=False, hata=mesaj), status

def metin(value, maximum, required=True):
    return isinstance(value, str) and len(value.strip()) <= maximum and (bool(value.strip()) or not required)

@pages.get('/')
def index():
    return render_template('index.html', demo=not current_app.config['GROQ_API_KEY'])

@pages.get('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@api.post('/sohbet')
def sohbet():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not metin(data.get('mesaj'), 2000):
        return hata('1–2000 karakterlik bir mesaj yazın.')
    history = data.get('gecmis', [])
    if not isinstance(history, list) or len(history) > 10:
        return hata('Sohbet geçmişi en fazla 10 mesaj içerebilir.')
    for item in history:
        if not isinstance(item, dict) or item.get('role') not in ('user', 'assistant') or not metin(item.get('content'), 3000):
            return hata('Sohbet geçmişi geçersiz.')
    history = [{'role': item['role'], 'content': item['content']} for item in history]
    try:
        return jsonify(basari=True, cevap=ai_service.yanit_uret(data['mesaj'].strip(), history), demo=not current_app.config['GROQ_API_KEY'])
    except AIServiceError:
        return hata('Asistan şu an yanıt veremiyor. Biraz sonra tekrar deneyin.', 503)

@api.post('/leads')
def lead_kaydet():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return hata('Geçerli bir form gönderin.')
    if not metin(data.get('isim'), 100) or not metin(data.get('telefon'), 25):
        return hata('Adınızı ve telefon numaranızı kontrol edin.')
    phone = data['telefon'].strip()
    if not re.fullmatch(r'[+\d\s().-]+', phone) or not 10 <= len(re.sub(r'\D', '', phone)) <= 15:
        return hata('Telefon numarası 10–15 rakam içermeli.')
    if not metin(data.get('mesaj', ''), 2000, required=False):
        return hata('Not en fazla 2000 karakter olabilir.')
    if data.get('onay') is not True:
        return hata('Geri dönüş talebini onaylamanız gerekiyor.')
    try:
        record_id = database.lead_ekle(data['isim'].strip(), phone, data.get('mesaj', '').strip())
        return jsonify(basari=True, id=record_id, mesaj='Talebiniz kaydedildi.'), 201
    except database.DatabaseError:
        return hata('Talebiniz kaydedilemedi. Lütfen tekrar deneyin.', 503)

@api.get('/leads')
def lead_listesi():
    # Kişisel bilgileri içeren liste yalnızca yönetici anahtarıyla okunabilir.
    expected = current_app.config['ADMIN_TOKEN']
    supplied = request.headers.get('Authorization', '').removeprefix('Bearer ')
    if not expected or not hmac.compare_digest(supplied.encode(), expected.encode()):
        return hata('Yönetici şifresi gerekli.', 401)
    try:
        return jsonify(basari=True, leadler=database.tum_leadler())
    except database.DatabaseError:
        return hata('Kayıtlar şu anda yüklenemiyor.', 503)
