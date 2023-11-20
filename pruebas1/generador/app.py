from flask import Flask, render_template, send_file
import secrets

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)