import 'package:dartz/dartz.dart';
import '../entities/user.dart';
import '../../../../core/errors/failures.dart';

/// Interfaccia del repository di autenticazione
/// Definisce COSA può fare il repository, ma non COME lo fa
/// L'implementazione concreta sarà nel data layer
abstract class AuthRepository {
  /// Effettua il login con username e password
  /// Ritorna Either<Failure, User>:
  /// - Left(Failure) se c'è un errore
  /// - Right(User) se il login ha successo
  Future<Either<Failure, User>> login(
    String username,
    String password);
  
  /// Effettua la registrazione con username, email e password
  Future<Either<Failure, User>> register(
    String username,
    String email,
    String password);
  
  /// Effettua il logout
  Future<Either<Failure, void>> logout();

  /// Ottiene l'utente attualmente autenticato
  Future<Either<Failure, User>> getCurrentUser();
}