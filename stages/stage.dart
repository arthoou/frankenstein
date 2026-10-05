import 'dart:io';

void main() {
  final input = stdin.readLineSync() ?? '';
  stdout.write('${input.trim()} -> Dart');
}
