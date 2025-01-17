import jwt
from time import time
from flask import current_app, flash


def create_token(user, expires_in=86400):
    with current_app.app_context():
        token = jwt.encode({'user': user, 'exp': time()+expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

def verify_token(token):
    with current_app.app_context():
        try:
            is_valid_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            flash('Link verifikasi sudah tidak aktif','error')
            return False
        except:
            flash('Link verifikasi tidak valid', 'error')
            return False
        return is_valid_token