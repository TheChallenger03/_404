"""
Applicazione Flask principale
Entry point del backend
"""

from flask import Flask
from flask_cors import CORS
from flask_session import Session

from config.settings import Config
from config import db, init_db
from api.auth import auth_bp

def create_app():
    """
    Factory function per creare l'app Flask
    
    Returns:
        Flask: Istanza dell'app configurata
    """

    # Crea l'app Flask
    app = Flask(__name__)

    # Carica la configurazione
    app.config.from_object(Config)
    Config.init_app(app)

    # Inizializza i CORS (permette richieste da frontend)
    CORS(app, 
        origins=Config.CORS_ORIGINS,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Inizializza la sessione
    Session(app)

    # Inizializza il database
    init_db(app)

    # Registra i Blueprint delle API
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        """Endpoint di test per verificare che il server sia attivo"""
        return {
            "message": "_404 Backend is running",
            "verision": "1.0.0"
        }
    
    @app.route('/health')
    def health():
        """Endpoint di controllo dello stato del server"""
        return {
            "status": "healthy",
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()

    print("\n" + "="*50)
    print("🎵 Music Player Backend")
    print("="*50)
    print("✅ Server avviato su http://localhost:5000")
    print("📚 API Endpoints disponibili:")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - POST /api/auth/logout")
    print("   - GET  /api/auth/me")
    print("="*50 + "\n")


    app.run(host='0.0.0.0',
            port=5000,
            debug=Config.DEBUG
    )   