from cryptography.fernet import Fernet
from config import get_settings
from fastapi import HTTPException

settings = get_settings()

SECRET_KEY = b'_7Wm40ZdLniIUfltI6GtVtNQ2gY3xwSu-W6hdn7diJU='
cipher_suite = Fernet(SECRET_KEY)

class Crypt:
    def encrypt(user_id, email):
        token_data = f"{email}:{user_id}".encode('utf-8')
        
        return cipher_suite.encrypt(token_data).decode('utf-8')

    
    def decrypt(token):
        try:
            decrypted_token = cipher_suite.decrypt(token.encode('utf-8'))
            email, user_id = decrypted_token.decode('utf-8').split(':')
        
            return [email, user_id]
        except Exception as e:
            raise HTTPException(status_code=403, detail='Invalid Token')