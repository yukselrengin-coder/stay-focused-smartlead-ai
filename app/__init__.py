import os
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from config import configurations
from .database import init_db

def create_app(test_config=None):
    app = Flask(__name__)
    mode = os.environ.get('APP_ENV', 'development')
    app.config.from_object(configurations[mode])
    if test_config:
        app.config.update(test_config)
    if not app.config['ADMIN_TOKEN'] or not app.config['SECRET_KEY']:
        raise RuntimeError('.env dosyasında SECRET_KEY ve ADMIN_TOKEN ayarlanmalı.')
    CORS(app, resources={r'/api/*': {'origins': app.config['CORS_ORIGINS']}}, allow_headers=['Content-Type', 'Authorization'])
    with app.app_context():
        init_db(app)
    from .routes import pages, api
    app.register_blueprint(pages)
    app.register_blueprint(api, url_prefix='/api')

    @app.get('/health')
    def health():
        return jsonify(basari=True, durum='aktif')

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(basari=False, hata='İstek işlenemedi.', kod=error.code), error.code

    @app.after_request
    def secure_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-store'
        return response

    return app
