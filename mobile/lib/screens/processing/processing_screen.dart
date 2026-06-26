import 'dart:async';
import 'package:flutter/material.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/models/response.dart';
import 'package:mobile/screens/result/result_screen.dart';

class ProcessingScreen extends StatefulWidget {
  final String requestId;

  const ProcessingScreen({super.key, required this.requestId});

  @override
  State<ProcessingScreen> createState() => _ProcessingScreenState();
}

class _ProcessingScreenState extends State<ProcessingScreen> {
  final ApiService _apiService = ApiService();
  Timer? _timer;
  String _currentStatus = 'Initializing...';
  String _currentAgent = '';
  int _progress = 0;
  bool _isNavigating = false;

  @override
  void initState() {
    super.initState();
    _startPolling();
  }

  void _startPolling() {
    _timer = Timer.periodic(const Duration(seconds: 2), (timer) {
      _pollStatus();
    });
    // Initial poll
    _pollStatus();
  }

  Future<void> _pollStatus() async {
    if (_isNavigating) return;

    try {
      final response = await _apiService.getStatus(widget.requestId);
      
      if (!mounted) return;

      setState(() {
        _currentStatus = response.status;
        _currentAgent = response.currentAgent;
        _progress = response.progress;
      });

      if (response.status.toUpperCase() == 'COMPLETED') {
        _isNavigating = true;
        _timer?.cancel();
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => ResultScreen(requestId: widget.requestId),
          ),
        );
      }
    } catch (e) {
      debugPrint('Polling error: $e');
    }
  }

  String _formatAgentName(String name) {
    if (name.isEmpty) return '';
    return name.split('_').map((word) {
      if (word.isEmpty) return word;
      return word[0].toUpperCase() + word.substring(1).toLowerCase();
    }).join(' ');
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analyzing'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                SizedBox(
                  height: 120,
                  width: 120,
                  child: CircularProgressIndicator(
                    value: _progress / 100,
                    strokeWidth: 8,
                    backgroundColor: Colors.grey[200],
                  ),
                ),
                Text(
                  '$_progress%',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 48),
            Text(
              'Processing Request',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'ID: ${widget.requestId}',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.grey),
            ),
            const SizedBox(height: 48),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceVariant.withOpacity(0.3),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Status:', style: TextStyle(color: Colors.grey)),
                      Text(
                        _currentStatus,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const Divider(height: 32),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Current Agent:', style: TextStyle(color: Colors.grey)),
                      Text(
                        _formatAgentName(_currentAgent),
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
