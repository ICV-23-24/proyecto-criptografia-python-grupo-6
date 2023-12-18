from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad,unpad
from base64 import b64encode, b64decode
import firebase_admin
from firebase_admin import credentials, firestore
from Crypto.PublicKey import RSA
# Importa módulos y funciones necesarios de la biblioteca Crypto
from Crypto.Cipher import DES3, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import base64


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

# Generar las claves privadas y publicas
def generar_claves_rsa():
    # Generar un par de claves RSA de 2048 bits
    par_claves = RSA.generate(2048)

    # Obtener la clave privada en formato PEM
    clave_privada = par_claves.export_key()
    
    # Obtener la clave pública en formato PEM
    clave_publica = par_claves.publickey().export_key()

    return clave_privada, clave_publica

# Registrarse en la base de datos
def agregarDatos(nombre, apellidos, email, password, nom_usu):
    # Generar claves antes de crear el diccionario de datos
    clave_privada, clave_publica = generar_claves_rsa()
    
    data = {'Nombre': nombre, 'Apellidos': apellidos, 'Email': email, 'Password': password,
            'Clave_Privada': clave_privada.decode('utf-8'), 'Clave_Publica': clave_publica.decode('utf-8')}
    
    doc_ref = db.collection('usuarios').document(str(nom_usu))
    
    # Verificar que el usuario no exista
    if doc_ref.get().exists:
        # Si existe:
        return print(f"Este nombre de usuario ya está en uso")
    else:
        # Si no existe:
        doc_ref.set(data)
        print("Usuario registrado con éxito")



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

# Función para generar una clave DES3 de 24 bytes
def generate_des_key():
    return get_random_bytes(24)

# Función para encriptar con una clave DES3
def encrypt_with_des_key(key, plaintext):
    cipher = DES3.new(key, DES3.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    # Convierte el resultado a Base64 para su representación como cadena
    return base64.b64encode(ciphertext).decode('utf-8')

# Función para desencriptar con una clave DES3
def decrypt_with_des_key(key, ciphertext):
    cipher = DES3.new(key, DES3.MODE_ECB)
    decrypted_text = cipher.decrypt(base64.b64decode(ciphertext)).decode('utf-8')
    return decrypted_text

# Función para generar un par de claves RSA de 2048 bits
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Función para encriptar con una clave pública RSA
def encrypt_with_rsa_public_key(public_key, plaintext):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    # Convierte el resultado a Base64 para su representación como cadena
    return base64.b64encode(ciphertext).decode('utf-8')

# Función para desencriptar con una clave privada RSA
def decrypt_with_rsa_private_key(private_key, ciphertext):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted_text = cipher.decrypt(base64.b64decode(ciphertext)).decode('utf-8')
    return decrypted_text