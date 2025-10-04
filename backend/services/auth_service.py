"""
Service per la gestione dell'autenticazione
Contiene la logica di business per login, register, ecc.
"""

import os
from models.user import User
from config import db
from config.settings import Config

class AuthService:
    """Service per operazioni di autenticazione"""

    @staticmethod
    def register_user(username, email, password):
        """
        Registra un nuovo utente
        
        Args:
            username: Nome utente
            email: Email
            password: Password in chiaro
        
        Returns:
            tuple: (User, error_message)
                Se successo: (User, None)
                Se errore: (None, "messaggio errore")
        """
        if not username:
            return None, "Username non valido"
        
        if not email or "@" not in email:
            return None, "Email non valida"
        
        if not password or len(password) < 6:
            return None, "Password troppo corta, minimo 6 caratteri"
        
        # Controlla se l'utente esiste già
        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            return None, "Utente con questo username già esistente"
        
        # Controlla se l'email esiste già
        existing_email = User.query.filter(User.email == email).first()
        if existing_email:
            return None, "Utente con questa email già esistente"
        
        try:
            # Crea il nuovo utente
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            # Crea la cartella per l'utente
            AuthService._create_user_folder(user.id)
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, f"Errore durante la registrazione: {str(e)}"
    
    @staticmethod
    def login_user(username, password):
        """
        Effettua il login di un utente
        
        Args:
            username: Nome utente
            password: Password in chiaro
        
        Returns:
            tuple: (User, error_message)
                Se successo: (User, None)
                Se errore: (None, "messaggio errore")
        """
        if not username or not password:
            return None, "Username e password richiesti"
        
        # Cerca l'utente per username
        user = User.query.filter(User.username == username).first()
        if not user or not user.check_password(password):
            return None, "Username o password errati"
        
        return user, None
    
    @staticmethod
    def _create_user_folder(user_id):
        """
        Crea la struttura di cartelle per l'utente
        
        Args:
            user_id: ID dell'utente
        """
        user_folder = os.path.join(Config.USER_STORAGE, user_id)
        playlists_folder = os.path.join(user_folder, "playlists")
    
        os.makedirs(user_folder, exist_ok=True)
        os.makedirs(playlists_folder, exist_ok=True)
        