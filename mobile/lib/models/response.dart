import 'dart:convert';

class TriageResponse {
  final String requestId;
  final String status;
  final String currentAgent;
  final int progress;
  final TriageResult? result;

  TriageResponse({
    required this.requestId,
    required this.status,
    required this.currentAgent,
    required this.progress,
    this.result,
  });

  factory TriageResponse.fromJson(Map<String, dynamic> json) {
    TriageResult? result;
    if (json.containsKey('output') && json['output'] != null) {
      result = TriageResult.fromJson(json['output']);
    }

    return TriageResponse(
      requestId: json['output']?['request_id']?.toString() ?? '',
      status: json['status']?.toString() ?? '',
      currentAgent: json['current_agent']?.toString() ?? '',
      progress: (json['progress'] as num?)?.toInt() ?? 0,
      result: result,
    );
  }
}

class ExecutionStep {
  final String name;
  final String status;
  final int durationMs;

  ExecutionStep({
    required this.name,
    this.status = 'completed',
    this.durationMs = 0,
  });

  factory ExecutionStep.fromJson(Map<String, dynamic> json) {
    return ExecutionStep(
      name: json['name']?.toString() ?? '',
      status: json['status']?.toString() ?? 'completed',
      durationMs: (json['duration_ms'] as num?)?.toInt() ?? 0,
    );
  }
}

class TriageResult {
  final String summary;
  final String riskLevel;
  final String recommendedNextStep;
  final String route;
  final String modelUsed;
  final String intent;
  final String urgency;
  final int complexity;
  final bool containsPii;
  final List<String> detectedEntities;
  final List<ExecutionStep> executionPath;
  final double latencyMs;

  TriageResult({
    required this.summary,
    required this.riskLevel,
    required this.recommendedNextStep,
    required this.route,
    required this.modelUsed,
    required this.intent,
    required this.urgency,
    required this.complexity,
    required this.containsPii,
    required this.detectedEntities,
    required this.executionPath,
    required this.latencyMs,
  });

  factory TriageResult.fromJson(dynamic input) {
    Map<String, dynamic> json;
    if (input is String) {
      json = jsonDecode(input) as Map<String, dynamic>;
    } else if (input is Map) {
      json = Map<String, dynamic>.from(input);
    } else {
      json = {};
    }

    // Check if the input is actually the status response wrapper
    if (json.containsKey('output') && json['output'] is Map) {
      json = Map<String, dynamic>.from(json['output']);
    }

    Map<String, dynamic> nestedResult = {};
    final rawResult = json['result'];
    if (rawResult is Map) {
      nestedResult = Map<String, dynamic>.from(rawResult);
    } else if (rawResult is String) {
      try {
        nestedResult = Map<String, dynamic>.from(jsonDecode(rawResult));
      } catch (_) {}
    }
    
    final List<ExecutionStep> steps = [];
    final rawPathData = json['execution_path'];
    List<dynamic> rawPath = [];
    if (rawPathData is List) {
      rawPath = rawPathData;
    } else if (rawPathData is String) {
      try {
        rawPath = jsonDecode(rawPathData) as List<dynamic>;
      } catch (_) {}
    }

    final Set<String> processedNormalizedNames = {};
    final Map<String, ExecutionStep> objectSteps = {};
    for (var item in rawPath) {
      if (item is Map) {
        final step = ExecutionStep.fromJson(Map<String, dynamic>.from(item));
        objectSteps[_normalize(step.name)] = step;
      }
    }

    String? lastString;
    for (var item in rawPath) {
      if (item is Map) {
        final step = ExecutionStep.fromJson(Map<String, dynamic>.from(item));
        final normalized = _normalize(step.name);
        if (!processedNormalizedNames.contains(normalized)) {
          steps.add(step);
          processedNormalizedNames.add(normalized);
        }
      } else if (item is String) {
        if (item == 'formatter' && lastString == 'formatter') continue;
        lastString = item;

        final normalized = _normalize(item);
        if (!processedNormalizedNames.contains(normalized)) {
          if (objectSteps.containsKey(normalized)) continue;
          steps.add(ExecutionStep(name: item));
          processedNormalizedNames.add(normalized);
        }
      }
    }

    return TriageResult(
      summary: nestedResult['summary']?.toString() ?? '',
      riskLevel: nestedResult['risk_level']?.toString() ?? 'Unknown',
      recommendedNextStep: nestedResult['recommended_next_step']?.toString() ?? '',
      route: json['route']?.toString() ?? '',
      modelUsed: json['model_used']?.toString() ?? '',
      intent: json['intent']?.toString() ?? '',
      urgency: json['urgency']?.toString() ?? '',
      complexity: (json['complexity'] as num?)?.toInt() ?? 0,
      containsPii: json['contains_pii'] == true,
      detectedEntities: (json['detected_entities'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
      executionPath: steps,
      latencyMs: (json['latency_ms'] as num?)?.toDouble() ?? 0.0,
    );
  }

  static String _normalize(String name) => name.replaceAll('_', '').toLowerCase();
}
