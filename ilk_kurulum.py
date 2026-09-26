"""Yeni bilgisayarda yerel ayarları oluşturur; mevcut ayarları korur."""
from pathlib import Path
import secrets


def hazirla(klasor):
    env = Path(klasor) / '.env'
    if env.exists():
        return False
    example = (Path(klasor) / '.env.example').read_text(encoding='utf-8')
    example = example.replace('replace-with-a-random-secret', secrets.token_urlsafe(40))
    example = example.replace('replace-with-a-long-private-password', secrets.token_urlsafe(32))
    # Exclusive creation also avoids overwriting a concurrently created file.
    with env.open('x', encoding='utf-8') as target:
        target.write(example)
    return True


if __name__ == '__main__':
    created = hazirla(Path(__file__).resolve().parent)
    print('Yerel ayarlar olusturuldu.' if created else 'Mevcut ayarlar korundu.')
    print('Yonetici sifreniz .env dosyasinin ADMIN_TOKEN satirindadir.')
