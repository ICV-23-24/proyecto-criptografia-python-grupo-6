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

# ---------------------------------------- VARIABLES GLOBALES ----------------------------------------

Id_usu= None

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
    # Verificar que el usuario no exista
    if doc_ref.get().exists:
        # Si existe:
        return print(f"Este nombre de ususario ya esta en uso")
    else:
        # Si no existe:
        doc_ref.set(data)


# Iniciar Sesion en la base de datos
def login(usuario,Passwd):
    try:
        # Obtén una referencia al documento
        doc_ref = db.collection('usuarios').document(usuario)

        # Verifica si el usuario es correcto
        if doc_ref.get().exists:
            print(f"El documento con ID '{usuario}' existe.")
            doc_data = doc_ref.get().to_dict()
            #Verificar si la cotraseña es correcta
            if doc_data and 'Password' in doc_data and doc_data['Password'] == Passwd:
                print(f"Inicio de sesion Correcto.")
                return usuario
            else:
                print(f"La password es incorrecta.")
                
        else:
            print(f"El usuario no existe en el sistema.")

    except Exception as e:
        print(f"Error al verificar las credenciales.")
