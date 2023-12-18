# Importa módulos y funciones necesarios de la biblioteca Crypto
from Crypto.Cipher import DES3, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import base64

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
