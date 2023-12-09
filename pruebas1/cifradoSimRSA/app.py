from flask import Flask, render_template, request, jsonify, send_file
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

app = Flask(__name__)

#RSA:
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_with_public_key(public_key, plaintext):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_with_private_key(private_key, ciphertext):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
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

    # Genera un par de claves
    private_key, public_key = generate_key_pair()

    # Cifra el contenido del archivo con la clave pública
    encrypted_content = encrypt_with_public_key(public_key, file_content)

    # Guarda el contenido cifrado en un nuevo archivo
    encrypted_filename = 'encrypted_' + file.filename
    with open(encrypted_filename, 'w') as encrypted_file:
        encrypted_file.write(encrypted_content)

    # Guarda la clave privada en un archivo
    private_key_filename = 'private_key.pem'
    with open(private_key_filename, 'w') as private_key_file:
        private_key_file.write(private_key.decode('utf-8'))

    return jsonify({'success': True, 'filename': encrypted_filename, 'private_key': private_key_filename})

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    private_key_filename = request.files['private_key'].filename
    ciphertext_filename = request.files['ciphertext'].filename

    # Lee la clave privada
    with open(private_key_filename, 'r') as private_key_file:
        private_key = private_key_file.read()

    # Lee el archivo cifrado
    with open(ciphertext_filename, 'r') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    # Descifra el contenido con la clave privada
    decrypted_content = decrypt_with_private_key(private_key, ciphertext)

    # Guarda el contenido descifrado en un nuevo archivo
    decrypted_filename = 'decrypted_' + os.path.basename(ciphertext_filename)[10:]  # Elimina 'encrypted_' del nombre original
    with open(decrypted_filename, 'w') as decrypted_file:
        decrypted_file.write(decrypted_content)

    return jsonify({'success': True, 'decrypted_filename': decrypted_filename})

if __name__ == '_main_':
    app.run(debug=True)