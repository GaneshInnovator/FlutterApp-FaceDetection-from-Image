import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: UploadImageScreen(),
    );
  }
}

class UploadImageScreen extends StatefulWidget {
  @override
  _UploadImageScreenState createState() => _UploadImageScreenState();
}

class _UploadImageScreenState extends State<UploadImageScreen> {
  final ImagePicker _picker = ImagePicker();
  String? _processedImage; // To hold the base64 string of the processed image

  Future<void> uploadImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      File imageFile = File(pickedFile.path);

      var request = http.MultipartRequest(
        'POST',
        Uri.parse('http://192.168.177.206:5000/process-image'), // Your server URL
      );

      request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));

      var response = await request.send();

      if (response.statusCode == 200) {
        var responseData = await http.Response.fromStream(response);
        var jsonData = jsonDecode(responseData.body);

        setState(() {
          _processedImage = jsonData['processedImage'];
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Image uploaded and processed')),
        );
      } else {
        print('Image upload failed');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Image upload failed')),
        );
      }
    } else {
      print('No image selected');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Upload Image')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: uploadImage,
              child: Text('Select and Upload Image'),
            ),
            SizedBox(height: 20),
            _processedImage != null
                ? Image.memory(
              base64Decode(_processedImage!),
              height: 200,
            )
                : Text('No processed image to display'),
          ],
        ),
      ),
    );
  }
}