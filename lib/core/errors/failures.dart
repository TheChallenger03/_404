/// Classe base per tutti i fallimenti nell'app
abstract class Failure {
  final String message;

  const Failure(this.message);

  @override
  String toString() => message;
}

/// Errore di rete (nessuna connessione, timeout, ecc.)
class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'Si è verificato un errore di rete. Si prega di controllare la connessione.']);
}

/// Errore del server (500, 502, ecc.)
class ServerFailure extends Failure {
  const ServerFailure([super.message = 'Si è verificato un errore del server. Riprova più tardi.']);
}

/// Errore di autenticazione (credenziali non valide, token scaduto, ecc.)
class AuthenticationFailure extends Failure {
  const AuthenticationFailure([super.message = 'Accesso non riuscito. Si prega di verificare le credenziali.']);
}

/// Errore generico
class UnknownFailure extends Failure {
  const UnknownFailure([super.message = 'Si è verificato un errore. Riprova più tardi.']);
}

/// Errore di validazione (input non valido, ecc.)
class ValidationFailure extends Failure {
  const ValidationFailure([super.message = 'Input non valido. Si prega di correggere e riprovare.']);
}