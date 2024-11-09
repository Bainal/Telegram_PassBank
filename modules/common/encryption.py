from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

encoding = "CP866"


# Функция для создания ключа на основе пароля
def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


# Функция для шифрования пароля
def encrypt_password(password: str, user_password: str) -> bytes:
    salt = os.urandom(16)
    key = generate_key(user_password, salt)
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return (salt + encrypted_password).decode(encoding)


# Функция для расшифровки пароля
def decrypt_password(decrypted_password: str, user_password: str) -> str:
    encrypted_data = decrypted_password.encode(encoding)
    salt = encrypted_data[:16]
    encrypted_password = encrypted_data[16:]
    key = generate_key(user_password, salt)
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode(encoding)
    return decrypted_password
