from flask import Flask, render_template, request, redirect, url_for, send_file
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import secrets

app = Flask(__name__)

def encrypt_image(image_path, password):
    with open(image_path, 'rb') as file:
        plaintext = file.read()

    key = password.encode()
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    encrypted_image_path = 'encrypted_image.png'
    with open(encrypted_image_path, 'wb') as file:
        file.write(ciphertext)

    return encrypted_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_clave')
def generar_clave_y_descargar():
    # Generar una clave aleatoria segura
    clave = secrets.token_hex(16)  # Tamaño de clave: 16 bytes

    # Escribir la clave en un archivo
    with open('clave_generada.txt', 'w') as archivo:
        archivo.write(clave)

    # Descargar el archivo generado
    return send_file('clave_generada.txt', as_attachment=True)

@app.route('/encrypt_image', methods=['POST'])
def encrypt_image_route():
    # Obtener la imagen subida por el usuario
    image_file = request.files['image']
    if not image_file or image_file.filename == '':
        return redirect(url_for('index'))

    image_path = 'original_image.png'
    image_file.save(image_path)

    # Obtener la contraseña del archivo
    password_file = request.files['password_file']
    if not password_file or password_file.filename == '':
        return redirect(url_for('index'))

    password = password_file.read().decode()

    # Encriptar la imagen
    encrypted_image_path = encrypt_image(image_path, password)

    return send_file(encrypted_image_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)