#   pip install --upgrade firebase-admin

import firebase_admin
from firebase_admin import credentials, firestore

# Conectar la clave d ela bd a mi app
cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

# Asignar cliente a la bd
db = firestore.client()

# Añadir datos a la bd
def agregarDatos(nombre,apellidos,email,password,nom_usu):
    data = {'Nombre':nombre,'Apellidos':apellidos,'Email':email,'Password':password}
    doc_ref = db.collection('usuarios').document(str(nom_usu))
    doc_ref.set(data)

agregarDatos('llubi','Ulinauskas','llubiulinauskas600@gmail.com','1234','Bollitto')