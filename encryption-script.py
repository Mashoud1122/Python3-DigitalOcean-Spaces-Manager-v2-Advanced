import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def create_private_key(file, verbose):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    keys = []
    pem_ar = str(pem,'utf-8')
    public_pem_ar = str(public_pem,'utf-8')
    keys.append(pem_ar)
    keys.append(public_pem_ar)

    with open(file + '_private_key.pem', 'wb') as f:
        f.write(pem)

    print("Private Key -> " + file + "_private_key.pem")

    with open(file + '_public_key.pem', 'wb') as f:
        f.write(public_pem)

    print("Public Key -> " + file + "_public_key.pem")
    return keys

def encrypt_text(text, public_key):
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted = public_key.encrypt(
        text,
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    return encrypted

def encrypt_file(file, public_key):
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    file = open(file, 'r')
    file = file.read()

    print(file)
    for line in file:
        encrypted = public_key.encrypt(
            bytes(file, 'utf-8'),
            padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )
        return encrypted

def decrypt_file(file, private_key):
    with open("person_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    encrypted = open(file, 'r')
    encrypted = encrypted.read()

    for line in encrypted:
        original_message = private_key.decrypt(
        bytes(line, 'utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )

me = decrypt_file("test3.txt", "person_private_key.pem")
print(me)
