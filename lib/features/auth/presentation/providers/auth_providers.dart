import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/network/api_client.dart';
import '../../data/repositories/auth_repository_impl.dart';
import '../../domain/repositories/auth_repository.dart';
import 'auth_state.dart';

/// Provider per ApiClient (singleton)
final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

/// Provider per SharedPreferences (singleton)
final sharedPreferencesProvider = FutureProvider<SharedPreferences>((ref) async {
  return await SharedPreferences.getInstance();
});

/// Provider per AuthRepository
/// Usa ApiClient e SharedPreferences
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  final sharedPreferences = ref.watch(sharedPreferencesProvider).value;
  if (sharedPreferences == null) {
    throw Exception('SharedPreferences non inizializzato');
  }
  return AuthRepositoryImpl(
    apiClient: apiClient,
    sharedPreferences: sharedPreferences,
  );
});

/// Provider per lo stato di autenticazione
/// Questo è il provider principale che gestisce login, register, logout
final authStateProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref)
    {
  final repository = ref.watch(authRepositoryProvider);
  return AuthNotifier(repository);
});

/// Notifier che gestisce lo stato di autenticazione
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repository;

  AuthNotifier(this._repository) : super(const AuthState.initial()) {
    // Controlla se c'è un utente già loggato quando l'app si avvia
    _checkCurrentUser();
  }

  Future<void> _checkCurrentUser() async {
    state = const AuthState.loading();

    final result = await _repository.getCurrentUser();

    result.fold(
      (failure) => state = const AuthState.initial(),
      (user) => state = AuthState.authenticated(user),
    );
  }

  Future<void> login(String username, String password) async {
    state = const AuthState.loading();

    final result = await _repository.login(username, password);

    result.fold(
      (failure) => state = AuthState.error(failure.message),
      (user) => state = AuthState.authenticated(user),
    );
  }

  Future<void> register(String username, String email, String password) async {
    state = const AuthState.loading();

    final result = await _repository.register(username, email, password);

    result.fold(
      (failure) => state = AuthState.error(failure.message),
      (user) => state = AuthState.authenticated(user),
    );
  }

  Future<void> logout() async {
    state = const AuthState.loading();

    final result = await _repository.logout();

    result.fold(
      (failure) => state = AuthState.error(failure.message),
      (_) => state = const AuthState.initial(),
    );
  }

  void clearError() {
    if (state.errorMessage != null) {
      state = state.copyWith(errorMessage: null);
    }
  }
}