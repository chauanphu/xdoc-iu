# utils/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from config.settings import settings

# Generate a key from the secret key in settings
def get_encryption_key():
    salt = b'xdoc_salt_for_encryption'  # In production, this should be stored securely
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(settings.jwt_secret_key.encode()))
    return key

# Create a Fernet cipher using the key
def get_cipher():
    key = get_encryption_key()
    return Fernet(key)

def encrypt_data(data: str) -> str:
    """Encrypt a string using Fernet symmetric encryption"""
    if not data:
        return data
    cipher = get_cipher()
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt a string that was encrypted with Fernet"""
    if not encrypted_data:
        return encrypted_data
    cipher = get_cipher()
    return cipher.decrypt(encrypted_data.encode()).decode()

def encrypt_dict_fields(data: dict, fields_to_encrypt: list) -> dict:
    """Encrypt specified fields in a dictionary"""
    result = data.copy()
    for field in fields_to_encrypt:
        if field in result and result[field]:
            result[field] = encrypt_data(str(result[field]))
    return result

def decrypt_dict_fields(data: dict, fields_to_decrypt: list) -> dict:
    """Decrypt specified fields in a dictionary"""
    result = data.copy()
    for field in fields_to_decrypt:
        if field in result and result[field]:
            result[field] = decrypt_data(result[field])
    return result