import 'dart:io';
import 'dart:typed_data';

void main() async{
  final File install = File(r"malware\install.cmd");
  final File rau = File(r"malware\install.cmd");

  final Uint8List installB = await install.readAsBytes();
  final Uint8List rauB = await rau.readAsBytes();

  bool space = false; 

  print("install : ");
  for (int i in installB) {
    stdout.write(i.toString());
    if (space) {
      stdout.write(" ");
    }
    space = !space;
  }
  print("\n\n");

  print("rau : ");
  space = false;
  for (int i in rauB) {
    stdout.write(i.toString());
    if (space) {
      stdout.write(" ");
    }
    space = !space;
  }

}
