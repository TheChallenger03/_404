import '../../domain/entities/user.dart';

/// Rappresenta lo stato dell'autenticazione nell'app
class AuthState {
  final User? user;
  final bool isLoading;
  final String? errorMessage;

  const AuthState({
    this.user,
    this.isLoading = false,
    this.errorMessage,
  });

  /// Stato iniziale (nessun utente, non sta caricando)
  const AuthState.initial()
      : user = null,
        isLoading = false,
        errorMessage = null;

  /// Stato di caricamento (sta facendo login/register)
  const AuthState.loading()
      : user = null,
        isLoading = true,
        errorMessage = null;

  /// Stato di errore (login/register fallito)
  const AuthState.error(this.errorMessage)
      : user = null,
        isLoading = false;

  /// Stato di successo (utente autenticato)
  const AuthState.authenticated(User this.user)
      : isLoading = false,
        errorMessage = null;
  
  /// Crea una copia dello stato con alcuni campi modificati
  AuthState copyWith({
    User? user,
    bool? isLoading,
    String? errorMessage,
  }) {
    return AuthState(
      user: user ?? this.user,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }

  /// Getter per sapere se l'utente è autenticato
  bool get isAuthenticated => user != null;
}