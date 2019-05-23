from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.fernet import Fernet

def encrypt(input_file, output_file, key):
    # key = b'' # Use one of the methods to get a key (it must be the same when decrypting)
    input_file = input_file
    cwd = os.getcwd()
    output_file = cwd + "/tmp/" + output_file

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

def decrypt(input_file, output_file, key):
    input_file = input_file
    output_file = output_file

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open(output_file, 'wb') as f:
        f.write("/tmp/" + encrypted)

# decrypt('text.enc', 'text.dec111', key)
