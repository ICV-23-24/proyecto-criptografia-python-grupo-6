from datetime import datetime
from flask import Flask, render_template, request
import secrets
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_contrasena')
def generar_contrasena():
    longitud_contraseña = 12
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena_generada = ''.join(secrets.choice(caracteres) for _ in range(longitud_contraseña))
    return contrasena_generada

if __name__ == '__main__':
    app.run(debug=True)
