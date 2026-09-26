"""SQL yalnızca bu katmanda bulunur."""
import sqlite3
from pathlib import Path
from flask import current_app, g

class DatabaseError(Exception):
    pass

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'], timeout=10)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)
    try:
        Path(app.config['DATABASE_URL']).parent.mkdir(parents=True, exist_ok=True)
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL, telefon TEXT NOT NULL,
            mesaj TEXT DEFAULT '', tarih TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        db.commit()
    except (sqlite3.Error, OSError) as exc:
        raise DatabaseError('Veritabanı hazırlanamadı.') from exc

def lead_ekle(isim, telefon, mesaj=''):
    try:
        db = get_db()
        # Kullanıcı bilgileri sorgu metnine eklenmez; ayrı parametre olarak verilir.
        cursor = db.execute('INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)', (isim, telefon, mesaj))
        db.commit()
        return cursor.lastrowid
    except sqlite3.Error as exc:
        if 'db' in g:
            g.db.rollback()
        raise DatabaseError('Kayıt kaydedilemedi.') from exc

def tum_leadler():
    try:
        return [dict(row) for row in get_db().execute('SELECT * FROM leads ORDER BY tarih DESC, id DESC').fetchall()]
    except sqlite3.Error as exc:
        raise DatabaseError('Kayıtlar okunamadı.') from exc
