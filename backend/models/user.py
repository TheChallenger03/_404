"""
Modello User per il database
Rappresenta un utente del sistema
"""

import uuid
import hashlib
from datetime import datetime, timezone
from config import db

class User(db.Model):
    """Modello User per il database"""

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, username, email, password):
        """
        Crea un nuovo utente
        
        Args:
            username: Nome utente
            email: Email
            password: Password in chiaro (verrà hashata)
        """
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """
        Imposta la password hashata
        Usa SHA-256 per l'hash
        
        Args:
            password: Password in chiaro
        """
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """
        Verifica se la password in chiaro corrisponde alla password hashata
        
        Args:
            password: Password in chiaro da verificare
        
        Returns:
            True se la password corrisponde, False altrimenti
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.password_hash == password_hash
    
    def to_dict(self):
        """
        Converte l'oggetto User in un dizionario (esclusa la password)
        
        Returns:
            Dizionario con i campi dell'utente (esclusa la password)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """Rappresentazione stringa dell'utente"""
        return f"<User {self.username}>"