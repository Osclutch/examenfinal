import os
from cryptography.fernet import Fernet
from PIL import Image
import requests

def encriptar_imagen(imagePath, key):
    with Image.open(imagePath) as img:
        

        img.save('temp.jpg', format= 'JPEG')
    
    with open('temp.jpg','rb') as f:

        imageData = f.read()

    cipher_suite = Fernet(key)
    datos_encriptados = cipher_suite.encrypt(imageData)    

    with open('imagen_encriptada.jpg' , 'wb') as f:
        f.write(datos_encriptados)

    os.remove('temp.jpg')
    return 'imagen_encriptada.jpg'

def encrypt_image_send(imagePath, key):
    encrypted_image_path = encriptar_imagen(imagePath, key)
    if not encrypted_image_path:
        return "Error en la encriptación de la imagen."

    try:

        with open(encrypted_image_path, 'rb') as f:
            files = {'file': (encrypted_image_path, f)}
            response = requests.post('http://localhost:5000/subir_imagen', files=files, data={'key': key})
        return response.text
    except requests.RequestException as e:
        return f"Error al enviar la imagen al servidor: {e}"

from cryptography.fernet import Fernet
import os

def seleccionar_imagen():
    
    path_imagen = input("Ingrese la ruta de la imagen: ")
    
    
    if not os.path.isfile(path_imagen):
        print("Error: El archivo especificado no existe o no es un archivo válido.")
        return None, None  

    
    generar_clave = input("¿Generar nueva clave de encriptación? (s/n): ").strip().lower()
    if generar_clave == 's':
        clave = Fernet.generate_key().decode() 
    elif generar_clave == 'n':
        clave = input("Ingrese la clave de encriptación: ").strip()  
    else:
        print("Respuesta no válida. Por favor, responda 's' o 'n'.")
        return None, None  

    return path_imagen, clave 

def main():
    imagePath, key = seleccionar_imagen()
    if imagePath and key:
        response = encrypt_image_send(imagePath, key)
        print(response)

if __name__ == '__main__':
    main()
    