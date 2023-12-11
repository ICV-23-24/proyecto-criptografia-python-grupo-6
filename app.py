from datetime import datetime
from flask import Flask, render_template, request
import functions as f
from firebase import firebase

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

if __name__ == '__main__':
    app.run(debug=True)