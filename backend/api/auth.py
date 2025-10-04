"""
API Endpoints per l'autenticazione
Gestisce login, register, logout
"""

from flask import Blueprint, request, session, jsonify
from services.auth_service import AuthService

# Crea il Blueprint per le rotte di autenticazione
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint per la registrazione
    
    Request Body (JSON):
        {
            "username": "mario",
            "email": "mario@example.com",
            "password": "password123"
        }
    
    Response (JSON):
        Success (201):
            {
                "success": true,
                "message": "Registrazione completata con successo",
                "user": {
                    "id": "...",
                    "username": "mario",
                    "email": "mario@example.com"
                }
            }
        
        Error (400):
            {
                "success": false,
                "message": "Messaggio di errore"
            }
    """
    try:
        # Ottieni i dati dalla richiesta
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False, 
                "message": "Dati mancanti"
            }), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Registra l'utente usando il service
        user, error = AuthService.register_user(username, email, password)
        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 400
        
        # Salva l'utente nella sessione (auto-login dopo registrazione)
        session['user_id'] = user.id

        return jsonify({
            "success": True,
            "message": "Registrazione completata con successo",
            "user": user.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Errore nel server: {str(e)}"
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint per il login
    
    Request Body (JSON):
        {
            "username": "mario",
            "password": "password123"
        }
    
    Response (JSON):
        Success (200):
            {
                "success": true,
                "message": "Login effettuato con successo",
                "user": {
                    "id": "...",
                    "username": "mario",
                    "email": "mario@example.com"
                }
            }
        
        Error (401):
            {
                "success": false,
                "message": "Credenziali non valide"
            }
    """
    try:
        # Ottieni i dati dalla richiesta
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False, 
                "message": "Dati mancanti"
            }), 400
        
        username = data.get('username')
        password = data.get('password')

        # Effettua il login usando il service
        user, error = AuthService.login_user(username, password)
        if error:
            return jsonify({
                "success": False,
                "message": error
            }), 401
        
        # Salva l'utente nella sessione
        session['user_id'] = user.id

        return jsonify({
            "success": True,
            "message": "Login effettuato con successo",
            "user": user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Errore nel server: {str(e)}"
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint per il logout
    
    Response (JSON):
        Success (200):
            {
                "success": true,
                "message": "Logout effettuato con successo"
            }
    """
    try:
        # Rimuovi l'utente dalla sessione
        session.pop('user_id', None)

        return jsonify({
            "success": True,
            "message": "Logout effettuato con successo"
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Errore nel server: {str(e)}"
        }), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Endpoint per ottenere l'utente corrente
    
    Response (JSON):
        Success (200):
            {
                "success": true,
                "user": {
                    "id": "...",
                    "username": "mario",
                    "email": "mario@example.com"
                }
            }
        
        Not authenticated (401):
            {
                "success": false,
                "message": "Non autenticato"
            }
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "message": "Non autenticato"
            }), 401
        
        user = AuthService.get_user_by_id(user_id)

        if not user:
            return jsonify({
                "success": False,
                "message": "Utente non trovato"
            }), 404
        
        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Errore nel server: {str(e)}"
        }), 500