import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/errors/failures.dart';
import '../../../../core/network/api_client.dart';
import '../../../../core/constants/api_constants.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../models/user_model.dart';

/// Implementazione concreta del repository di autenticazione
/// Gestisce la comunicazione con il server e lo storage locale
class AuthRepositoryImpl implements AuthRepository {
  final ApiClient apiClient;
  final SharedPreferences sharedPreferences;

  // Chiavi per salvare dati localmente
  static const String _userIdKey = 'USER_ID';
  static const String _usernameKey = 'USERNAME';
  static const String _emailKey = 'EMAIL';

  AuthRepositoryImpl({
    required this.apiClient,
    required this.sharedPreferences,
  });

  @override
  Future<Either<Failure, User>> login(String username, String password) async {
    try {
      final response = await apiClient.post(
        ApiConstants.loginEndpoint,
        data: {
          'username': username,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final userModel = UserModel.fromJson(response.data);
        // Salva i dati dell'utente localmente
        await _saveUserLocally(userModel);
        return Right(userModel);
      } else {
        return Left(AuthenticationFailure('Credenziali non valide.'));
      }
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> register(
    String username,
    String email,
    String password,
  ) async {
    try {
      final response = await apiClient.post(
        ApiConstants.registerEndpoint,
        data: {
          'username': username,
          'email': email,
          'password': password,
        },
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        final userModel = UserModel.fromJson(response.data['user']);
        // Salva i dati dell'utente localmente
        await _saveUserLocally(userModel);
        return Right(userModel);
      } else {
        return Left(ServerFailure(response.data['message'] ?? 'Errore durante la registrazione.'));
      }
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      // Chiama l'API di logout (per invalidare la sessione sul server)
      await apiClient.post(ApiConstants.logoutEndpoint);

      // Rimuovi i dati dell'utente salvati localmente
      await _clearUserLocally();

      return const Right(null);
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      await _clearUserLocally();
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> getCurrentUser() async {
    try {
      final userId = sharedPreferences.getString(_userIdKey);
      final username = sharedPreferences.getString(_usernameKey);
      final email = sharedPreferences.getString(_emailKey);

      if (userId != null && username != null && email != null) {
        return Right(
          User(
            id: userId, 
            username: username, 
            email: email
          ),
        );
      } else {
        return Left(AuthenticationFailure('Nessun utente autenticato.'));
      }
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  Future<void> _saveUserLocally(UserModel user) async {
    await sharedPreferences.setString(_userIdKey, user.id);
    await sharedPreferences.setString(_usernameKey, user.username);
    await sharedPreferences.setString(_emailKey, user.email);
  }

  Future<void> _clearUserLocally() async {
    await sharedPreferences.remove(_userIdKey);
    await sharedPreferences.remove(_usernameKey);
    await sharedPreferences.remove(_emailKey);
  }

  Failure _handleDioError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:

      case DioExceptionType.sendTimeout:

      case DioExceptionType.receiveTimeout:
        return const NetworkFailure('Timeout di connessione. Si prega di riprovare.');

      case DioExceptionType.badResponse:
        final statusCode = e.response?.statusCode;
        if (statusCode == 401 || statusCode == 403) {
          return AuthenticationFailure(
            e.response?.data['message'] ?? 'Accesso non autorizzato. Si prega di verificare le credenziali.',
          );
        }
        return ServerFailure(
          e.response?.data['message'] ?? 'Errore del server. Riprova più tardi.',
        );

      case DioExceptionType.cancel:
        return const UnknownFailure('Richiesta annullata.');

      default:
        return const NetworkFailure('Si è verificato un errore di rete. Si prega di controllare la connessione.');
    }
  }
}