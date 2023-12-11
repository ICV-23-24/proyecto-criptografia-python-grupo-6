# Importación de módulos necesarios desde el framework Flask
from flask import Flask, render_template, request, redirect, url_for, send_file
# Importación de módulos para criptografía
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# Importación de módulo para operaciones con el sistema operativo y generación segura de valores aleatorios
import os
# Importación de módulo para generación segura de claves
import secrets

# Creación de la aplicación Flask
app = Flask(__name__)


# Función para encriptar una imagen utilizando AES en modo CFB
def encrypt_image(image_path, password):
    with open(image_path, 'rb') as file:
        plaintext = file.read()

    # Convertir la contraseña en una clave
    key = password.encode()
    # Crear un cifrador con el algoritmo AES y el modo CFB
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())
    # Inicializar el cifrador para encriptar
    encryptor = cipher.encryptor()
    # Encriptar el texto plano
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Guardar el texto cifrado en un nuevo archivo
    encrypted_image_path = 'encrypted_image.png'
    with open(encrypted_image_path, 'wb') as file:
        file.write(ciphertext)

    return encrypted_image_path

    # Convertir la contraseña en una clave
    key = password.encode()
    # Crear un cifrador con el algoritmo AES y el modo CFB
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())

    # Guardar el texto plano en un nuevo archivo
    decrypted_image_path = 'decrypted_image.png'
    with open(decrypted_image_path, 'wb') as file:
        file.write(plaintext)

    return decrypted_image_path

# Ruta principal, devuelve la plantilla 'index_symmetric.html'
@app.route('/')
def index():
    return render_template('index_symmetric.html')

# Ruta para generar una clave aleatoria segura y descargarla
@app.route('/generar_clave')
def generar_clave_y_descargar():
    # Generar una clave aleatoria segura
    clave = secrets.token_hex(16)  # Tamaño de clave: 16 bytes

    # Escribir la clave en un archivo
    with open('clave_generada.txt', 'w') as archivo:
        archivo.write(clave)

    # Descargar el archivo generado
    return send_file('clave_generada.txt', as_attachment=True)

# Ruta para encriptar una imagen
@app.route('/encrypt_image', methods=['POST'])
def encrypt_image_route():
    # Obtener la imagen subida por el usuario
    image_file = request.files['image']
    if not image_file or image_file.filename == '':
        return redirect(url_for('index'))

    # Guardar la imagen en el servidor
    image_path = 'original_image.png'
    image_file.save(image_path)

    # Obtener la contraseña del archivo
    password_file = request.files['password_file']
    if not password_file or password_file.filename == '':
        return redirect(url_for('index'))

    # Leer la contraseña desde el archivo
    password = password_file.read().decode()

    # Encriptar la imagen y obtener la ruta del archivo encriptado
    encrypted_image_path = encrypt_image(image_path, password)

    # Enviar el archivo encriptado como respuesta al usuario
    return send_file(encrypted_image_path, as_attachment=True)
#desencriptar
@app.route('/Decrypt_image', methods=['POST'])

def decrypt_image_route():
    # Obtener la imagen subida por el usuario
    image_file = request.files['image']
    if not image_file or image_file.filename == '':
        return redirect(url_for('index'))

def desencriptar_imagen(clave, iv, imagen_cifrada):
    backend = default_backend()

    # Crear un objeto de contexto de cifrado
    cipher = Cipher(algorithms.AES(clave), modes.CFB(iv), backend=backend)

    # Crear un objeto de descifrado
    decryptor = cipher.decryptor()

    # Desencriptar la imagen
    imagen_descifrada = decryptor.update(imagen_cifrada) + decryptor.finalize()

    return imagen_descifrada

# Ejecutar la aplicación si este script es el programa principal
if __name__ == "_main_":
    app.run(debug=True)