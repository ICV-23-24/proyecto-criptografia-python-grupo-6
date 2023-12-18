# Importa los módulos y funciones necesarios
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from functions import generate_des_key, encrypt_with_des_key, decrypt_with_des_key, generate_rsa_key_pair, encrypt_with_rsa_public_key, decrypt_with_rsa_private_key

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Configura la carpeta de descargas para almacenar archivos
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
app.config["UPLOAD_FOLDER"] = DOWNLOAD_FOLDER

# Ruta principal: Renderiza el formulario en index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la encriptación, se ejecuta al enviar el formulario de encriptación
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Obtiene el archivo y el algoritmo del formulario
    file = request.files['file']
    algorithm = request.form['algorithm']
    file_content = file.read().decode('utf-8')

    # Selecciona el algoritmo y genera claves según sea necesario
    if algorithm == 'des':
        key = generate_des_key()
        encrypted_content = encrypt_with_des_key(key, file_content)
        key_filename = 'des_key.key'
    elif algorithm == 'rsa':
        private_key, public_key = generate_rsa_key_pair()
        encrypted_content = encrypt_with_rsa_public_key(public_key, file_content)
        key_filename = 'rsa_key.pem'

    # Define nombres y rutas de archivos
    encrypted_filename = 'encrypted_' + file.filename
    encrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
    with open(encrypted_filepath, 'w') as encrypted_file:
        encrypted_file.write(encrypted_content)

    key_filepath = os.path.join(app.config['UPLOAD_FOLDER'], key_filename)
    with open(key_filepath, 'wb') as key_file:
        key_file.write(key if algorithm == 'des' else private_key)

    # Retorna una respuesta JSON indicando el éxito de la operación
    return jsonify({'success': True, 'filename': encrypted_filename, 'key_filename': key_filename})

# Ruta para descargar archivos desde la carpeta de descargas
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Ruta para la desencriptación, se ejecuta al enviar el formulario de desencriptación
@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Obtiene la información necesaria del formulario
    key_filename = request.files['key'].filename
    ciphertext_filename = request.files['ciphertext'].filename
    algorithm = request.form['algorithm']

    # Lee la clave y el archivo cifrado desde la carpeta de descargas
    key_filepath = os.path.join(app.config['UPLOAD_FOLDER'], key_filename)
    with open(key_filepath, 'rb') as key_file:
        key = key_file.read()

    ciphertext_filepath = os.path.join(app.config['UPLOAD_FOLDER'], ciphertext_filename)
    with open(ciphertext_filepath, 'r') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    # Descifra el contenido con la clave según el algoritmo seleccionado
    if algorithm == 'des':
        decrypted_content = decrypt_with_des_key(key, ciphertext)
    elif algorithm == 'rsa':
        decrypted_content = decrypt_with_rsa_private_key(key, ciphertext)

    # Define nombres y rutas de archivos
    decrypted_filename = 'decrypted_' + os.path.basename(ciphertext_filename)[10:]
    decrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], decrypted_filename)
    with open(decrypted_filepath, 'w') as decrypted_file:
        decrypted_file.write(decrypted_content)

    # Retorna una respuesta JSON indicando el éxito de la operación
    return jsonify({'success': True, 'decrypted_filename': decrypted_filename})

# Inicia la aplicación Flask en modo de depuración si se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
