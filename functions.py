from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
import firebase_admin
from firebase_admin import credentials, firestore

# Conectar la clave de la bd a mi app
cred = credentials.Certificate("bd/clave.json")
firebase_admin.initialize_app(cred)

# Asignar cliente a la bd
db = firestore.client()

# ---------------------------------------- FUNCIONES ----------------------------------------

# Encriptar mensaje Simetrico
def encrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return b64encode(encrypted_message).decode('utf-8')

# Desencriptar mensaje Simetrico
def decrypt_message(message, key):
    key = key.encode('utf-8')
    cipher = AES.new(pad(key, AES.block_size), AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(b64decode(message)), AES.block_size).decode('utf-8')
    return decrypted_message

# Registrarse en la base de datos
def agregarDatos(nombre,apellidos,email,password,nom_usu):
    data = {'Nombre':nombre,'Apellidos':apellidos,'Email':email,'Password':password}
    doc_ref = db.collection('usuarios').document(str(nom_usu))
    doc_ref.set(data)