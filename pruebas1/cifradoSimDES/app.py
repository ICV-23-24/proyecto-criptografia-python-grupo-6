from flask import Flask, render_template, request, jsonify, send_file
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64
import os

app = Flask(__name__)

# DES:
def generate_key():
    return get_random_bytes(24)  # Clave de 24 bytes para DES3

def encrypt_with_key(key, plaintext):
    cipher = DES3.new(key, DES3.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_with_key(key, ciphertext):
    cipher = DES3.new(key, DES3.MODE_ECB)
    decrypted_text = cipher.decrypt(base64.b64decode(ciphertext)).decode('utf-8')
    return decrypted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['file']

    # Lee el contenido del archivo
    file_content = file.read().decode('utf-8')

    # Genera una clave
    key = generate_key()

    # Cifra el contenido del archivo con la clave
    encrypted_content = encrypt_with_key(key, file_content)

    # Guarda el contenido cifrado en un nuevo archivo
    encrypted_filename = 'encrypted_' + file.filename
    with open(encrypted_filename, 'w') as encrypted_file:
        encrypted_file.write(encrypted_content)

    # Guarda la clave en un archivo
    key_filename = 'des_key.key'
    with open(key_filename, 'wb') as key_file:
        key_file.write(key)

    return jsonify({'success': True, 'filename': encrypted_filename, 'key_filename': key_filename})

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    key_filename = request.files['key'].filename
    ciphertext_filename = request.files['ciphertext'].filename

    # Lee la clave
    with open(key_filename, 'rb') as key_file:
        key = key_file.read()

    # Lee el archivo cifrado
    with open(ciphertext_filename, 'r') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    # Descifra el contenido con la clave
    decrypted_content = decrypt_with_key(key, ciphertext)

    # Guarda el contenido descifrado en un nuevo archivo
    decrypted_filename = 'decrypted_' + os.path.basename(ciphertext_filename)[10:]  # Elimina 'encrypted_' del nombre original
    with open(decrypted_filename, 'w') as decrypted_file:
        decrypted_file.write(decrypted_content)

    return jsonify({'success': True, 'decrypted_filename': decrypted_filename})

if __name__ == '__main__':
    app.run(debug=True)