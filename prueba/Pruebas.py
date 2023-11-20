import secrets
import string

def generar_contrasena(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

# Especifica la longitud de la contraseña que deseas generar
longitud_contraseña = 12  # Puedes ajustar la longitud según tus necesidades

# Genera una contraseña aleatoria
contrasena_generada = generar_contrasena(longitud_contraseña)

print("Contraseña generada:", contrasena_generada)