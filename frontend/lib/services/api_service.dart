import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/models.dart';

class ApiService {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );
  
  static Future<bool> testConnection() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
  
  static Future<IdentifyResponse> identifyCar(
    String code, {
    int? year,
    String? series,
    String? color,
    String? seriesNumber,
  }) async {
    try {
      final queryParams = <String, String>{};
      if (year != null) queryParams['year'] = year.toString();
      if (series != null && series.isNotEmpty) queryParams['series'] = series;
      if (color != null && color.isNotEmpty) queryParams['color'] = color;
      if (seriesNumber != null && seriesNumber.isNotEmpty) queryParams['series_number'] = seriesNumber;
      
      final uri = Uri.parse('$baseUrl/identify/$code').replace(queryParameters: queryParams);
      
      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw Exception('Connection timeout. Check if backend is running at $baseUrl');
        },
      );
      
      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return IdentifyResponse.fromJson(jsonData);
      } else if (response.statusCode == 404) {
        throw Exception('Car not found');
      } else {
        throw Exception('Failed to identify car: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error identifying car: $e');
    }
  }
  
  static Future<CollectionItem> addToCollection(String variantId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/collection'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'variant_id': variantId}),
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw Exception('Connection timeout. Check if backend is running at $baseUrl');
        },
      );
      
      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return CollectionItem.fromJson(jsonData);
      } else {
        throw Exception('Failed to add to collection: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error adding to collection: $e');
    }
  }
  
  static Future<List<CollectionItem>> getCollection() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/collection'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw Exception(
            'Connection timeout.\n\n'
            'Troubleshooting:\n'
            '1. Make sure backend is running: cd backend && ./run_server.sh\n'
            '2. Check if IP address is correct: $baseUrl\n'
            '3. Ensure phone and computer are on the same WiFi network\n'
            '4. Try accessing $baseUrl in your phone\'s browser'
          );
        },
      );
      
      if (response.statusCode == 200) {
        final List<dynamic> jsonData = json.decode(response.body);
        return jsonData.map((item) => CollectionItem.fromJson(item)).toList();
      } else {
        throw Exception('Failed to get collection: ${response.statusCode}');
      }
    } on SocketException catch (e) {
      throw Exception(
        'Cannot connect to backend server.\n\n'
        'Error: ${e.message}\n\n'
        'Troubleshooting:\n'
        '1. Backend URL: $baseUrl\n'
        '2. Make sure backend is running: cd backend && ./run_server.sh\n'
        '3. Check if IP address is correct (find your computer\'s IP)\n'
        '4. Ensure phone and computer are on the same WiFi network\n'
        '5. For Android Emulator, use: http://10.0.2.2:8000\n'
        '6. Check firewall settings on your computer'
      );
    } catch (e) {
      if (e.toString().contains('SocketException') || 
          e.toString().contains('Failed host lookup') ||
          e.toString().contains('No route to host')) {
        throw Exception(
          'Cannot connect to backend server.\n\n'
          'Troubleshooting:\n'
          '1. Backend URL: $baseUrl\n'
          '2. Make sure backend is running: cd backend && ./run_server.sh\n'
          '3. Check if IP address is correct (find your computer\'s IP)\n'
          '4. Ensure phone and computer are on the same WiFi network\n'
          '5. For Android Emulator, use: http://10.0.2.2:8000\n'
          '6. Check firewall settings on your computer'
        );
      }
      throw Exception('Error getting collection: $e');
    }
  }
  
}
