import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

secret_key_str = os.getenv("ENCRYPTION_KEY")
if not secret_key_str:
    raise ValueError("Error: You have ENCRYPTION_KEY in .env??")


f_instance = Fernet(secret_key_str.encode('utf-8'))


class EncryptionPassword:
    def __init__(self):
        self.key = f_instance
        pass

    def encode(self, password: str):
        token = self.key.encrypt(password.encode("utf-8"))
        return token.decode("utf-8")

    def decode(self, token: str):
        decrypted_bytes = self.key.decrypt(token.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")