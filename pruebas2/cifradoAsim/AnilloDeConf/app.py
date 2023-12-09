from flask import Flask, render_template, request
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# Almacenar las claves en memoria (no seguro para producción)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form['message']

    # Encriptar utilizando la clave pública
    encrypted_message = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=padding.SHA256()),
            algorithm=padding.SHA256(),
            label=None
        )
    )

    return render_template('index.html', public_key=public_key, encrypted_message=encrypted_message)

if __name__ == '__main__':
    app.run(debug=True)