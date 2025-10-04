/// Rappresenta un utente del sistema
/// Questa è l'entità "pura" che rappresenta il concetto di utente
class User {
  final String id;
  final String email;
  final String username;

  User({
    required this.id,
    required this.email,
    required this.username,
  });

  /// Crea una copia dell'utente con alcuni campi modificati
  User copyWith({
    String? id,
    String? email,
    String? username,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      username: username ?? this.username,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'User{id: $id, email: $email, username: $username}';
  }
}