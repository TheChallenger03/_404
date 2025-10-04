"""
Modulo di configurazione
Inizializza SQLAlchemy e fornisce funzioni di setup
"""

import os
from flask_sqlalchemy import SQLAlchemy

# Inizializza SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Inizializza il database con l'app Flask
    
    Args:
        app: Istanza Flask
    """
    # Estrai il percorso del database dalla configurazione
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"🔍 Database URI: {db_uri}")
    
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        db_path = os.path.abspath(db_path)  # Converti in percorso assoluto
        db_dir = os.path.dirname(db_path)
        
        print(f"🔍 Database path: {db_path}")
        print(f"🔍 Database directory: {db_dir}")
        
        # Crea la directory del database se non esiste
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            print(f"✅ Directory database verificata/creata: {db_dir}")
        
        # Aggiorna la URI con il percorso assoluto
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    db.init_app(app)
    
    with app.app_context():
        # Importa i modelli per creare le tabelle
        from models.user import User
        
        # Crea tutte le tabelle
        db.create_all()
        
        print("✅ Database inizializzato con successo")
