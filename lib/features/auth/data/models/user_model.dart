import '../../domain/entities/user.dart';

/// Modello che rappresenta l'utente come arriva dal server (JSON)
/// Estende l'entità User e aggiunge la logica di conversione JSON
class UserModel extends User {
  UserModel({
    required super.id,
    required super.email,
    required super.username,
  });

  /// Crea un'istanza di UserModel da una mappa JSON
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      username: json['username'] as String,
    );
  }

   /// Converte il UserModel in JSON (per inviare al server)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
    };
  }

  /// Converte il Model in Entity (per il domain layer)
  User toEntity() {
    return User(
      id: id,
      email: email,
      username: username,
    );
  }

  /// Crea un UserModel da un'entità User
  factory UserModel.fromEntity(User user) {
    return UserModel(
      id: user.id,
      email: user.email,
      username: user.username,
    );
  }
}