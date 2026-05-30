import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key-for-dev'
    
    # Veritabanı URL'sini al, yoksa SQLite'a düş
    db_url = os.environ.get('DATABASE_URL') or os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        
    # Render'dan gelen PostgreSQL linkleri genelde postgres:// ile başlar.
    # Yeni SQLAlchemy sürümleri postgresql:// beklediği için bunu otomatik düzeltiyoruz.
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
