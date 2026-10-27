import 'package:flutter/material.dart';

import '../models/models.dart';
import '../services/api_service.dart';

class AddModelScreen extends StatefulWidget {
  const AddModelScreen({super.key});

  @override
  State<AddModelScreen> createState() => _AddModelScreenState();
}

class _AddModelScreenState extends State<AddModelScreen> {
  final _codeController = TextEditingController();
  bool _isLoading = false;
  String? _error;

  Future<void> _findModel() async {
    final code = _codeController.text.trim();
    if (code.isEmpty || _isLoading) return;

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final result = await ApiService.identifyCar(code);
      if (!mounted) return;

      if (result.car.variants.isEmpty) {
        setState(() => _error = 'No variants found for this model.');
        return;
      }

      final variant = result.car.variants.length == 1
          ? result.car.variants.first
          : await _selectVariant(result.car, result.car.variants);

      if (variant != null && mounted) {
        await ApiService.addToCollection(variant.id);
        if (mounted) {
          _codeController.clear();
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Added to collection.')),
          );
        }
      }
    } catch (error) {
      if (mounted) setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<Variant?> _selectVariant(Car car, List<Variant> variants) {
    return showModalBottomSheet<Variant>(
      context: context,
      builder: (context) => SafeArea(
        child: ListView(
          shrinkWrap: true,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
              child: Text(
                car.name,
                style: Theme.of(context).textTheme.titleLarge,
              ),
            ),
            ...variants.map(
              (variant) => ListTile(
                title: Text(variant.desc),
                subtitle: Text(variant.toyNumber),
                trailing: variant.isChase
                    ? const Chip(label: Text('CHASE'))
                    : null,
                onTap: () => Navigator.pop(context, variant),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _codeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add a model'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Enter the model number from the packaging.',
                  style: Theme.of(context).textTheme.titleMedium,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                TextField(
                  controller: _codeController,
                  textCapitalization: TextCapitalization.characters,
                  textInputAction: TextInputAction.search,
                  onSubmitted: (_) => _findModel(),
                  decoration: const InputDecoration(
                    labelText: 'Model number',
                    hintText: 'HYW54',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                FilledButton.icon(
                  onPressed: _isLoading ? null : _findModel,
                  icon: _isLoading
                      ? const SizedBox.square(
                          dimension: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.search),
                  label: Text(_isLoading ? 'Searching…' : 'Find model'),
                ),
                if (_error != null) ...[
                  const SizedBox(height: 16),
                  Text(
                    _error!,
                    style: TextStyle(color: Theme.of(context).colorScheme.error),
                    textAlign: TextAlign.center,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
