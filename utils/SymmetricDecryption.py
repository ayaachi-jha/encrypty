import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import PySimpleGUI as sg
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.fernet import Fernet, InvalidToken



def fernetDecrypt(input_file, key, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    actualdata = data[16:]
    fernet = Fernet(key)

    #output_file = f"Dec-{input_file}"

    try:

        decrypted = fernet.decrypt(actualdata)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

    except:
        print("Invalid Key")
        sg.popup('INVALID KEY')


def aesDecrypt(data, key, output_file):
    print("AES-CBC DECRYPTION")
    actualdata = data[16:-16]
    iv = data[-16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    try:
        decrypted = decryptor.update(actualdata) + decryptor.finalize()
        with open(output_file, 'wb') as f:
            f.write(decrypted)
        print("AES-CBC DECRYPTION SUCCESSFUL")
    except:
        print("INVALID KEY")
        sg.popup('INVALID KEY')


def chacha20poly1305Decrypt(data, key, aad, output_file):
    print("CHACHA20POLY1305 DECRYPTION")
    chacha = ChaCha20Poly1305(key)
    nonce = data[-12:]
    actualdata = data[16:-12]
    try:
        decrypted = chacha.decrypt(nonce, actualdata, aad)
        with open(output_file, 'wb') as f:
            f.write(decrypted)
        print("CHACHA20POLY1305 DECRYPTION SUCCESSFUL")
    except:
        print("EITHER INVALID KEY OR INVALID ASSOCIATED DATA")
        sg.popup('EITHER INVALID KEY OR INVALID ASSOCIATED DATA')
