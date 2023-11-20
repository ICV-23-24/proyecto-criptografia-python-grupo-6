from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    password = request.form['password']
    file = request.files['file']

    if file:
        # Generar una clave a partir de la contraseña
        key = base64.urlsafe_b64encode(password.encode())
        cipher = Fernet(key)

        # Leer la imagen y cifrar con la clave generada
        encrypted_data = cipher.encrypt(file.read())

        # Guardar los datos cifrados temporalmente (mejora para un entorno de producción)
        encrypted_filename = 'encrypted_image.enc'
        with open(encrypted_filename, 'wb') as f:
            f.write(encrypted_data)

        return render_template('index.html', encrypted=True, encrypted_filename=encrypted_filename)
    else:
        return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    password = request.form['password']
    encrypted_filename = request.form['encrypted_filename']

    if encrypted_filename:
        # Generar la clave a partir de la contraseña
        key = base64.urlsafe_b64encode(password.encode())
        cipher = Fernet(key)

        # Leer los datos cifrados y descifrar con la clave generada
        with open(encrypted_filename, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        # Guardar la imagen desencriptada temporalmente (mejora para un entorno de producción)
        decrypted_filename = 'decrypted_image.png'
        with open(decrypted_filename, 'wb') as f:
            f.write(decrypted_data)

        return render_template('index.html', decrypted=True, decrypted_filename=decrypted_filename)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)