"""
Configurazione dell'applicazione
Gestisce variabili d'ambiente e impostazioni
"""
import os
from dotenv import load_dotenv

load_dotenv()  # Carica variabili d'ambiente da un file .env

class Config:
    """Classe di configurazione per l'app Flask"""
    
    # Debug mode
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
    
    # Secret key per sessioni e sicurezza
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Configurazione del database
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "storage", "database", "_404.db")}'
    )
    SQLALCHELMY_TRACK_MODIFICATIONS = False

    # Configurazione della sessione
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'storage', 'sessions')
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 86400 * 30  # 30 giorni in secondi

    # Configurazione upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'storage', 'temp')
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024  # 15 MB
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

    # Percorsi storage
    MUSIC_STORAGE = os.path.join(BASE_DIR, 'storage', 'music')
    USER_STORAGE = os.path.join(BASE_DIR, 'storage', 'users')
    DATABASE_IMAGES = os.path.join(BASE_DIR, 'storage', 'database', 'images')

    # Configurazione CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    @staticmethod
    def init_app(app):
        """Inizializza l'app con la configurazione"""
        # Crea la directory del database
        db_dir = os.path.join(Config.BASE_DIR, 'storage', 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # Crea le altre directory
        os.makedirs(Config.SESSION_FILE_DIR, exist_ok=True)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MUSIC_STORAGE, exist_ok=True)
        os.makedirs(Config.USER_STORAGE, exist_ok=True)
        os.makedirs(Config.DATABASE_IMAGES, exist_ok=True)