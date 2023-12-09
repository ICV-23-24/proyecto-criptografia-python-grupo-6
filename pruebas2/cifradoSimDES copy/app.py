from flask import Flask, render_template, request, jsonify, send_file
from cryptography.fernet import Fernet
import base64
import os

app = Flask(__name__)

# Fernet:
def generate_key():
    return Fernet.generate_key()

def encrypt_with_key(key, plaintext):
    cipher = Fernet(key)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_with_key(key, ciphertext):
    cipher = Fernet(key)
    decrypted_text = cipher.decrypt(base64.b64decode(ciphertext)).decode('utf-8')
    return decrypted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['file']

    # Read the content of the file
    file_content = file.read().decode('utf-8')

    # Generate a symmetric key
    symmetric_key = generate_key()

    # Encrypt the content of the file with the symmetric key
    encrypted_content = encrypt_with_key(symmetric_key, file_content)

    # Save the encrypted content in a new file
    encrypted_filename = 'encrypted_' + file.filename
    with open(encrypted_filename, 'w') as encrypted_file:
        encrypted_file.write(encrypted_content)

    # Save the symmetric key in a file
    key_filename = 'symmetric_key.key'
    with open(key_filename, 'wb') as key_file:
        key_file.write(symmetric_key)

    return jsonify({'success': True, 'filename': encrypted_filename, 'key_filename': key_filename})

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/download/<filename>')
def download_key(filename):
    return send_file(filename, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    key_filename = request.files['key'].filename
    ciphertext_filename = request.files['ciphertext'].filename

    # Read the symmetric key
    with open(key_filename, 'rb') as key_file:
        symmetric_key = key_file.read()

    # Read the encrypted file
    with open(ciphertext_filename, 'r') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    # Decrypt the content with the symmetric key
    decrypted_content = decrypt_with_key(symmetric_key, ciphertext)

    # Save the decrypted content in a new file
    decrypted_filename = 'decrypted_' + os.path.basename(ciphertext_filename)[10:]  # Elimina 'encrypted_' del nombre original
    with open(decrypted_filename, 'w') as decrypted_file:
        decrypted_file.write(decrypted_content)

    return jsonify({'success': True, 'decrypted_filename': decrypted_filename})

if __name__ == '__main__':
    app.run(debug=True)