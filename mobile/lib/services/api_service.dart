import 'package:dio/dio.dart';
import 'package:mobile/models/request.dart';
import 'package:mobile/models/response.dart';
import 'package:mobile/core/api/api_constants.dart';

class ApiService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: ApiConstants.baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ),
  );

  Future<String> submitTriage(TriageRequest request) async {
    try {
      final Map<String, dynamic> data = {
        'content': request.text,
      };

      if (request.imagePath != null) {
        data['file'] = await MultipartFile.fromFile(
          request.imagePath!,
          filename: request.imagePath!.split('/').last,
        );
      }

      final formData = FormData.fromMap(data);

      final response = await _dio.post(
        ApiConstants.triageEndpoint,
        data: formData,
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return response.data['request_id']?.toString() ?? '';
      } else {
        throw Exception('Server returned status ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Unexpected error: $e');
    }
  }

  Future<TriageResponse> getStatus(String requestId) async {
    try {
      final response = await _dio.get('${ApiConstants.statusEndpoint}/$requestId');
      
      if (response.statusCode == 200) {
        return TriageResponse.fromJson(response.data);
      } else {
        throw Exception('Server returned status ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Unexpected error: $e');
    }
  }

  Future<TriageResult> getResult(String requestId) async {
    try {
      final response = await _dio.get('${ApiConstants.statusEndpoint}/$requestId');
      
      if (response.statusCode == 200) {
        return TriageResult.fromJson(response.data);
      } else {
        throw Exception('Server returned status ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      throw Exception('Unexpected error: $e');
    }
  }
}
