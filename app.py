import os
import random
import cirq
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import io


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class CaesarCipher:
    @staticmethod
    def encrypt(text, shift):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                if char.islower():
                    encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                else:
                    encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text

    @staticmethod
    def decrypt(text, shift):
        return CaesarCipher.encrypt(text, -shift)

class QuantumCipher:
    @staticmethod
    def process(binary_message, key):
        n = len(binary_message)
        qubits = [cirq.LineQubit(i) for i in range(n)]
        circuit = cirq.Circuit()

        for i, bit in enumerate(binary_message):
            if bit == '1':
                circuit.append(cirq.X(qubits[i]))

        for i, bit in enumerate(key):
            if bit == '1':
                circuit.append(cirq.X(qubits[i]))

        circuit.append(cirq.measure(*qubits, key='result'))
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)
        measurements = result.measurements['result'][0]
        return ''.join(str(b) for b in measurements)

class BinaryConverter:
    @staticmethod
    def text_to_binary(text):
        return ''.join(format(ord(char), '08b') for char in text)

    @staticmethod
    def binary_to_text(binary):
        text = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            text += chr(int(byte, 2))
        return text

class KeyGenerator:
    @staticmethod
    def generate(length):
        return ''.join(random.choice(['0', '1']) for _ in range(length))

class ImageSteganography:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def encode_message(image_path, message, output_path):
        img = Image.open(image_path)
        binary_message = BinaryConverter.text_to_binary(message) + '1111111111111110'  # Delimiter
        pixels = img.load()
        width, height = img.size
        idx = 0
        for i in range(width):
            for j in range(height):
                if idx < len(binary_message):
                    pixel = list(pixels[i, j])
                    for k in range(3):  # RGB channels
                        if idx < len(binary_message):
                            pixel[k] = pixel[k] & ~1 | int(binary_message[idx])
                            idx += 1
                    pixels[i, j] = tuple(pixel)
                else:
                    break
        img.save(output_path)

    @staticmethod
    def decode_message(image_path):
        img = Image.open(image_path)
        pixels = img.load()
        width, height = img.size
        binary_message = ""
        for i in range(width):
            for j in range(height):
                pixel = list(pixels[i, j])
                for k in range(3):  # RGB channels
                    binary_message += str(pixel[k] & 1)
        binary_message = binary_message.split('1111111111111110')[0]
        return BinaryConverter.binary_to_text(binary_message)


saved_key = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crypto')
def crypto():
    return render_template('crypto.html')

@app.route('/steganography')
def steganography():
    return render_template('steganography.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    global saved_key
    encrypted_text_caesar = ""
    encrypted_text_quantum = ""
    key = ""
    if request.method == 'POST':
      if 'text' in request.form:
        text = request.form['text']
        shift = int(request.form['shift'])
        encrypted_caesar = CaesarCipher.encrypt(text, shift)
        binary_message = BinaryConverter.text_to_binary(encrypted_caesar)
        key = KeyGenerator.generate(len(binary_message))
        saved_key = key
        encrypted_quantum = QuantumCipher.process(binary_message, key)

        encrypted_text_caesar = encrypted_caesar
        encrypted_text_quantum = encrypted_quantum

        return render_template('encrypt.html', encrypted_text_caesar=encrypted_text_caesar, encrypted_text_quantum=encrypted_text_quantum, key=key)
    
    return render_template('encrypt.html', encrypted_text_caesar=encrypted_text_caesar, encrypted_text_quantum=encrypted_text_quantum, key=key)

@app.route('/download_encrypt', methods=['POST'])
def download_encrypt():
  filename = request.form.get('filename', 'encrypted_data.txt')
  encrypted_text_quantum = request.form.get('encrypted_text_quantum')
  
  file_io = io.BytesIO(encrypted_text_quantum.encode('utf-8'))
  
  return send_file(file_io, as_attachment=True, download_name=filename)


@app.route('/download_key', methods=['POST'])
def download_key():
    filename = request.form.get('key_filename', 'key.txt')
    key = request.form.get('key')
    
    file_io = io.BytesIO(key.encode('utf-8'))
    return send_file(file_io, as_attachment=True, download_name=filename)


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    global saved_key
    decrypted_text = ""
    if request.method == 'POST':
        input_key = ""
        if 'key_file' in request.files:
             key_file = request.files['key_file']
             if key_file.filename != '':
                key_filename = secure_filename(key_file.filename)
                key_file_path = os.path.join(app.config['UPLOAD_FOLDER'], key_filename)
                key_file.save(key_file_path)

                try:
                    with open(key_file_path, 'r') as kf:
                        input_key = kf.read().strip()
                except FileNotFoundError:
                    return render_template('decrypt.html', error="File kunci tidak ditemukan!")

        elif 'key' in request.form:
             input_key = request.form.get('key')
        
        if 'load_file' in request.files:
            file = request.files['load_file']
            if file.filename != '':
                 filename = secure_filename(file.filename)
                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                 file.save(file_path)

                 try:
                     with open(file_path, 'r') as f:
                       lines = f.readlines()
                       if len(lines) >= 1:
                         encrypted_text_quantum = lines[0].strip()
                         shift = int(request.form.get('shift',0))
                         
                         if input_key != saved_key:
                            return render_template('decrypt.html', error="Kunci tidak valid!")
                         
                         decrypted_quantum = QuantumCipher.process(encrypted_text_quantum, input_key)
                         decrypted_text_caesar = BinaryConverter.binary_to_text(decrypted_quantum)
                         decrypted_text = CaesarCipher.decrypt(decrypted_text_caesar, shift)
                       else:
                            return render_template('decrypt.html', error="File tidak valid formatnya!")
                 except FileNotFoundError:
                   return render_template('decrypt.html', error="File tidak ditemukan!")

            else:
                encrypted_text = request.form['encrypted_text']
                shift = int(request.form.get('shift', 0))

                if input_key != saved_key:
                    return render_template('decrypt.html', error="Kunci tidak valid!")

                decrypted_quantum = QuantumCipher.process(encrypted_text, input_key)
                decrypted_text_caesar = BinaryConverter.binary_to_text(decrypted_quantum)
                decrypted_text = CaesarCipher.decrypt(decrypted_text_caesar, shift)
        elif 'encrypted_text' in request.form:
           encrypted_text = request.form['encrypted_text']
           shift = int(request.form.get('shift', 0))
           if input_key != saved_key:
                 return render_template('decrypt.html', error="Kunci tidak valid!")

           decrypted_quantum = QuantumCipher.process(encrypted_text, input_key)
           decrypted_text_caesar = BinaryConverter.binary_to_text(decrypted_quantum)
           decrypted_text = CaesarCipher.decrypt(decrypted_text_caesar, shift)

        if 'save_text' in request.form:
            filename = request.form.get('filename', 'decrypted_message.txt')
            file_io = io.BytesIO(decrypted_text.encode('utf-8'))
            return send_file(file_io, as_attachment=True, download_name=filename)

    return render_template('decrypt.html', decrypted_text=decrypted_text)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    global saved_key
    encrypted_text_quantum = ""
    key = ""
    image_path = ""
    output_image_path = ""
    original_size = 0
    encrypted_size = 0
    if request.method == 'POST':
        if 'image' not in request.files:
             return render_template('insert.html', image_path=image_path, encrypted_text_quantum=encrypted_text_quantum, key=key, encrypted_image=output_image_path, original_size=original_size, encrypted_size=encrypted_size)
         
        image = request.files['image']
        if image.filename == '':
             return render_template('insert.html', image_path=image_path, encrypted_text_quantum=encrypted_text_quantum, key=key, encrypted_image=output_image_path, original_size=original_size, encrypted_size=encrypted_size)

        if image and ImageSteganography.allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            original_size = os.path.getsize(image_path)
            text = request.form['text']
            shift = int(request.form['shift'])

            encrypted_caesar = CaesarCipher.encrypt(text, shift)
            binary_message = BinaryConverter.text_to_binary(encrypted_caesar)
            key = KeyGenerator.generate(len(binary_message))
            saved_key = key
            encrypted_quantum = QuantumCipher.process(binary_message, key)

            output_filename = "encrypted_" + filename
            output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            ImageSteganography.encode_message(image_path, encrypted_quantum, output_image_path)
            encrypted_text_quantum = encrypted_quantum
            encrypted_size = os.path.getsize(output_image_path)


            return render_template('insert.html', encrypted_text_quantum=encrypted_text_quantum, key=key,
                                   original_image=image_path, encrypted_image=output_image_path, success="Pesan berhasil disisipkan!", filename=output_filename, original_size=original_size, encrypted_size=encrypted_size)


        else:
            return render_template('insert.html', image_path=image_path, encrypted_text_quantum=encrypted_text_quantum, key=key, encrypted_image=output_image_path, original_size=original_size, encrypted_size=encrypted_size)

    return render_template('insert.html', image_path=image_path, encrypted_text_quantum=encrypted_text_quantum, key=key, encrypted_image=output_image_path, original_size=original_size, encrypted_size=encrypted_size)


@app.route('/download_image', methods=['POST'])
def download_image():
  filename = request.form.get('filename')
  encrypted_image = request.form.get('encrypted_image')
  
  return send_file(encrypted_image, as_attachment=True, download_name=filename)

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    global saved_key
    decrypted_text = ""
    image_path = ""
    if request.method == 'POST':
      shift = int(request.form.get('shift', 0))
      if 'image' not in request.files:
        return render_template('extract.html', error="Tidak ada file gambar terunggah.")

      image = request.files['image']

      if image.filename == '':
        return render_template('extract.html', error="Tidak ada file gambar terpilih.")

      if image and ImageSteganography.allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        input_key = ""
        if 'key_file' in request.files:
            key_file = request.files['key_file']
            if key_file.filename != '':
                 key_filename = secure_filename(key_file.filename)
                 key_file_path = os.path.join(app.config['UPLOAD_FOLDER'], key_filename)
                 key_file.save(key_file_path)

                 try:
                     with open(key_file_path, 'r') as kf:
                        input_key = kf.read().strip()
                 except FileNotFoundError:
                     return render_template('extract.html', error="File kunci tidak ditemukan!")
            
        elif 'key' in request.form:
             input_key = request.form['key']
          
        extracted_binary = ImageSteganography.decode_message(image_path)
        
        if len(input_key) != len(extracted_binary):
           return render_template('extract.html', decrypted_text="", original_image=image_path, error="Panjang Kunci tidak sesuai!")

        if input_key != saved_key:
            return render_template('extract.html', decrypted_text="", original_image=image_path, error="Kunci tidak valid!")

        decrypted_quantum = QuantumCipher.process(extracted_binary, input_key)
        decrypted_text_caesar = BinaryConverter.binary_to_text(decrypted_quantum)
        decrypted_text = CaesarCipher.decrypt(decrypted_text_caesar, shift)

        return render_template('extract.html', decrypted_text=decrypted_text, original_image=image_path, filename="extracted_message.txt")


      else:
        return render_template('extract.html', error="Tipe file tidak diizinkan")
    return render_template('extract.html', decrypted_text=decrypted_text, filename="extracted_message.txt")

@app.route('/download_extract_text', methods=['POST'])
def download_extract_text():
  filename = request.form.get('filename')
  decrypted_text = request.form.get('decrypted_text')

  file_content = f"Pesan terdekripsi: {decrypted_text}"
  file_io = io.BytesIO(file_content.encode('utf-8'))
  
  return send_file(file_io, as_attachment=True, download_name=filename)


if __name__ == '__main__':
    app.run(debug=True)