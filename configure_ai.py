"""Anahtarı sohbet geçmişine veya komut satırına yazmadan yerelde kaydet."""
from getpass import getpass
from pathlib import Path
import secrets
from dotenv import dotenv_values, set_key


def main():
    env_path = Path(__file__).resolve().parent / '.env'
    print('Groq API anahtarini asagida girin. Yazarken ekranda gorunmez.')
    print('Iptal etmek icin bos birakip Enter tusuna basin.')
    key = getpass('API anahtari: ').strip()
    if not key:
        print('Iptal edildi. Mevcut ayarlar degistirilmedi.')
        return
    if not key.startswith('gsk_') or len(key) < 20 or any(c.isspace() for c in key):
        print('Bu deger bir Groq anahtarina benzemiyor. Hicbir ayar degistirilmedi.')
        return
    settings = dotenv_values(env_path) if env_path.exists() else {}
    # Diğer ayarları koru. Anahtarı veya dosya içeriğini ekrana yazma.
    for name in ('SECRET_KEY', 'ADMIN_TOKEN'):
        if not settings.get(name):
            set_key(env_path, name, secrets.token_urlsafe(40))
    set_key(env_path, 'GROQ_API_KEY', key)
    set_key(env_path, 'AI_PROVIDER', 'groq')
    print('Anahtar yerel .env dosyasina kaydedildi; henuz API ile dogrulanmadi.')
    print('Uygulamayi kapatip BASLAT.cmd ile yeniden acin.')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nIslem iptal edildi.')
    except OSError:
        print('Ayar dosyasi kaydedilemedi. Klasorun yazma izinlerini kontrol edin.')
