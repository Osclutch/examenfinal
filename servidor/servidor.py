from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

@app.route('/subir_imagen', methods = ['POST'])

def subir_imagen():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if 'key' not in request.form:
        return jsonify({'error': 'No encryption key provided'}), 400
    
    encryption_key_client = request.form['key'].encode()
    
    llave = request.form['key']
    try:
        cipher_suite_client = Fernet(encryption_key_client)
        imagen_encriptada = file.read()
        imagen_desencriptada = cipher_suite_client.decrypt(imagen_encriptada)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    output_filename = f"imagen_desencriptada_{os.urandom(6).hex()}.jpg"
    with open(output_filename, 'wb') as f:
        f.write(imagen_desencriptada)

    return jsonify({'mensaje': 'Imagen desencriptada correctamente'})
    

if __name__ == '__main__':
    app.run(debug=True)       