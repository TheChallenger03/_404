class ApiConstants {
  static const String localUrl = 'http://localhost:8000';
  static const String remoteUrl = 'http://192.168.1.66:8000'; // aldariel.servemp3.com
  static const String androidEmulatorUrl = 'http://10.0.2.2:8000';
  static const String baseUrl = remoteUrl;
  
  // Auth endpoints
  static const String loginEndpoint = '/api/auth/login';
  static const String registerEndpoint = '/api/auth/register';
  static const String logoutEndpoint = '/api/auth/logout';
  
  // Songs endpoints
  static const String songsEndpoint = '/api/songs';
  static const String songDetailEndpoint = '/api/songs/';
  
  // Playlists endpoints
  static const String playlistsEndpoint = '/api/playlists';
  
  // Upload endpoints
  static const String uploadEndpoint = '/api/upload';
  
  // Timeout
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}