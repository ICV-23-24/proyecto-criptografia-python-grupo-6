from datetime import datetime
from flask import Flask, render_template, request
import functions as f
from firebase import firebase
from flask import Flask, render_template, request
# Importa los módulos y funciones necesarios
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from functions import generate_des_key, encrypt_with_des_key, decrypt_with_des_key, generate_rsa_key_pair, encrypt_with_rsa_public_key, decrypt_with_rsa_private_key

app = Flask(__name__)

nombre_coleccion = "usuarios"

firebase_config = {
    "apiKey": "AIzaSyD3IkiTKoTPCXVhQkMEFnqDPOX27LgdcLg",
    "authDomain": "grupo-6-b1e81.firebaseapp.com",
    "databaseURL": "G-CKHV8LXBMB",
    "projectId": "grupo-6-b1e81",
    "storageBucket": "grupo-6-b1e81.appspot.com",
    "messagingSenderId": "663980461078",
    "appId": "1:663980461078:web:48667350aef455874e3937"
}

fb = firebase.FirebaseApplication("https://" + firebase_config["projectId"] + ".firebaseio.com/", None)

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home2/")
def home2():
    return render_template("home2.html")

# Encriptacion simetrica
@app.route("/csimetrico/", methods=['GET','POST'])
def csimetrico():
    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']
        mode = request.form['mode']

        if mode == 'encrypt':
            encrypted_message = f.encrypt_message(message, key)
            return render_template('csimetrico.html', encrypted_message=encrypted_message, mode=mode)
        elif mode == 'decrypt':
            decrypted_message = f.decrypt_message(message, key)
            return render_template('csimetrico.html', decrypted_message=decrypted_message, mode=mode)

    return render_template("csimetrico.html")


#Encriptacion Asimetrica
@app.route("/casimetrico/")
def casimetrico():
    return render_template("casimetrico.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/doc/")
def doc():
    return render_template("doc.html")

@app.route("/sesion/", methods=['GET','POST'])
def sesion(): 
    if request.method == 'POST':
        usuario = request.form['nomUsu']
        Passwd = request.form['Passwd']

        f.Id_usu = f.login(usuario,Passwd)
        if f.Id_usu == None:
            return render_template("home.html")
        else :
            print (f"Bienvenido {f.Id_usu} :)")
            return render_template("home2.html")
    return render_template("sesion.html")

@app.route("/registro/", methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['Nom']
        apellidos = request.form['Ape']
        usuario = request.form['NomUsu']
        Email = request.form['Email']
        Passwd = request.form['Passwd']

        f.agregarDatos(nombre,apellidos,Email,Passwd,usuario)        

        return render_template("home.html")

    return render_template("registro.html")
        
        

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

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


if __name__ == '__main__':
    app.run(debug=True)