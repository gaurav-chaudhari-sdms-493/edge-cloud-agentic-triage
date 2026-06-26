import 'package:flutter/material.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/models/response.dart';

class ResultScreen extends StatefulWidget {
  final String requestId;

  const ResultScreen({super.key, required this.requestId});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  final ApiService _apiService = ApiService();
  late Future<TriageResult> _resultFuture;

  @override
  void initState() {
    super.initState();
    _resultFuture = _apiService.getResult(widget.requestId);
  }

  String _formatAgentName(String name) {
    final normalized = name.replaceAll('_', '').toLowerCase();
    
    const Map<String, String> displayNames = {
      'validation': 'Validation',
      'ocr': 'OCR',
      'piidetection': 'PII Detection',
      'piisanitization': 'PII Sanitization',
      'intentclassification': 'Intent Classification',
      'medicalcomplexity': 'Medical Complexity',
      'urgencyassignment': 'Urgency Assignment',
      'router': 'Router',
      'medicalreasoning': 'Medical Reasoning',
      'formatter': 'Formatter',
      'auditlogger': 'Audit Logger',
    };

    if (displayNames.containsKey(normalized)) {
      return displayNames[normalized]!;
    }

    return name.split('_').map((word) {
      if (word.isEmpty) return word;
      return word[0].toUpperCase() + word.substring(1).toLowerCase();
    }).join(' ');
  }

  String _formatDuration(int ms) {
    if (ms >= 1000) {
      return '${(ms / 1000).toStringAsFixed(1)} s';
    }
    return '$ms ms';
  }

  String _formatLatency(double ms) {
    if (ms >= 1000) {
      return '${(ms / 1000).toStringAsFixed(2)} s';
    }
    return '${ms.toInt()} ms';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.surface,
      appBar: AppBar(
        title: const Text('Triage Assessment'),
        centerTitle: true,
      ),
      body: FutureBuilder<TriageResult>(
        future: _resultFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.error_outline, color: Colors.red, size: 48),
                    const SizedBox(height: 16),
                    Text('Error: ${snapshot.error}', textAlign: TextAlign.center),
                    const SizedBox(height: 24),
                    ElevatedButton(
                      onPressed: () => setState(() {
                        _resultFuture = _apiService.getResult(widget.requestId);
                      }),
                      child: const Text('Retry'),
                    )
                  ],
                ),
              ),
            );
          } else if (!snapshot.hasData) {
            return const Center(child: Text('No data found'));
          }

          final result = snapshot.data!;
          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildRiskLevelHeader(result.riskLevel),
                const SizedBox(height: 16),
                _buildSectionHeader('Clinical Summary'),
                _buildSummaryCard(result.summary),
                const SizedBox(height: 16),
                _buildSectionHeader('Recommendation'),
                _buildRecommendationCard(result.recommendedNextStep),
                if (result.detectedEntities.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  _buildSectionHeader('Detected Entities'),
                  _buildEntitiesCard(result.detectedEntities),
                ],
                const SizedBox(height: 16),
                _buildSectionHeader('Analysis Insights'),
                _buildInsightsGrid(result),
                const SizedBox(height: 16),
                _buildSectionHeader('System Details'),
                _buildDetailsCard(result),
                const SizedBox(height: 16),
                _buildSectionHeader('Agent Execution Timeline'),
                _buildExecutionPathCard(result.executionPath),
                const SizedBox(height: 32),
                FilledButton.tonal(
                  onPressed: () => Navigator.of(context).popUntil((route) => route.isFirst),
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: const Text('New Triage Request'),
                ),
                const SizedBox(height: 32),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 8, top: 8),
      child: Text(
        title.toUpperCase(),
        style: Theme.of(context).textTheme.labelLarge?.copyWith(
              color: Theme.of(context).colorScheme.primary,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.2,
            ),
      ),
    );
  }

  Widget _buildRiskLevelHeader(String riskLevel) {
    Color riskColor;
    IconData riskIcon;
    switch (riskLevel.toUpperCase()) {
      case 'HIGH':
        riskColor = Colors.red;
        riskIcon = Icons.warning_rounded;
        break;
      case 'MEDIUM':
        riskColor = Colors.orange;
        riskIcon = Icons.info_rounded;
        break;
      case 'LOW':
        riskColor = Colors.green;
        riskIcon = Icons.check_circle_rounded;
        break;
      default:
        riskColor = Colors.blue;
        riskIcon = Icons.help_outline_rounded;
    }

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: riskColor.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: riskColor.withValues(alpha: 0.3)),
      ),
      child: Row(
        children: [
          Icon(riskIcon, color: riskColor, size: 32),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Assessment Result',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: Colors.black54),
                ),
                Text(
                  '$riskLevel Risk Level',
                  style: TextStyle(
                    color: riskColor,
                    fontWeight: FontWeight.bold,
                    fontSize: 22,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSummaryCard(String summary) {
    return Card(
      elevation: 0,
      color: Theme.of(context).colorScheme.surfaceContainerHigh,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Text(
          summary,
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(height: 1.6),
        ),
      ),
    );
  }

  Widget _buildRecommendationCard(String recommendation) {
    return Card(
      elevation: 0,
      color: Theme.of(context).colorScheme.primaryContainer.withValues(alpha: 0.4),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(Icons.medical_services, color: Theme.of(context).colorScheme.primary),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                recommendation,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                      color: Theme.of(context).colorScheme.onPrimaryContainer,
                    ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEntitiesCard(List<String> entities) {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: entities.map((entity) => Chip(
        label: Text(entity, style: const TextStyle(fontSize: 12)),
        backgroundColor: Theme.of(context).colorScheme.surfaceContainerHigh,
        side: BorderSide.none,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      )).toList(),
    );
  }

  Widget _buildInsightsGrid(TriageResult result) {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: 2.2,
      children: [
        _buildInsightItem(
          Icons.psychology_alt,
          'Intent',
          result.intent.toUpperCase(),
          result.intent.toLowerCase() == 'emergency' ? Colors.red : Colors.blue,
        ),
        _buildInsightItem(
          Icons.speed,
          'Urgency',
          result.urgency.toUpperCase(),
          result.urgency.toLowerCase() == 'high' || result.urgency.toLowerCase() == 'emergency' ? Colors.orange : Colors.green,
        ),
        _buildInsightItem(
          Icons.layers,
          'Complexity',
          'Level ${result.complexity}',
          Colors.purple,
        ),
        _buildInsightItem(
          Icons.security,
          'PII Status',
          result.containsPii ? 'CONTAINS PII' : 'CLEAN',
          result.containsPii ? Colors.orange : Colors.green,
        ),
      ],
    );
  }

  Widget _buildInsightItem(IconData icon, String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Row(
        children: [
          Icon(icon, size: 20, color: color),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(label, style: const TextStyle(fontSize: 10, color: Colors.black54)),
                Text(
                  value,
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: color),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailsCard(TriageResult result) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: Theme.of(context).colorScheme.outlineVariant),
      ),
      child: Padding(
        padding: const EdgeInsets.all(8),
        child: Column(
          children: [
            _buildDetailRow(Icons.route, 'Routing Decision', result.route),
            _buildDetailRow(Icons.smart_toy_outlined, 'Triage Model', result.modelUsed),
            _buildDetailRow(Icons.timer_outlined, 'Total Processing', _formatLatency(result.latencyMs)),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value) {
    return ListTile(
      dense: true,
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(icon, size: 18),
      ),
      title: Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      subtitle: Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
    );
  }

  Widget _buildExecutionPathCard(List<ExecutionStep> steps) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: Theme.of(context).colorScheme.outlineVariant),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: steps.asMap().entries.map((entry) {
            final index = entry.key;
            final step = entry.value;
            final isLast = index == steps.length - 1;

            return IntrinsicHeight(
              child: Row(
                children: [
                  Column(
                    children: [
                      Container(
                        width: 14,
                        height: 14,
                        decoration: BoxDecoration(
                          color: Theme.of(context).colorScheme.primary,
                          shape: BoxShape.circle,
                          border: Border.all(color: Colors.white, width: 2),
                          boxShadow: [
                            BoxShadow(
                              color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.3),
                              blurRadius: 4,
                            )
                          ],
                        ),
                      ),
                      if (!isLast)
                        Expanded(
                          child: Container(
                            width: 2,
                            color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.2),
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Padding(
                      padding: EdgeInsets.only(bottom: isLast ? 0 : 20.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                _formatAgentName(step.name),
                                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                              ),
                              Text(
                                step.status.toUpperCase(),
                                style: TextStyle(
                                  color: Colors.green.shade700,
                                  fontSize: 10,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ],
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: Colors.grey.shade100,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              _formatDuration(step.durationMs),
                              style: TextStyle(
                                color: Theme.of(context).colorScheme.primary,
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}
