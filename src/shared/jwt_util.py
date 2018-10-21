import jwt

from src.server.server import app
from datetime import datetime, timedelta

class JwtUtil:

    @staticmethod
    def encode(sub):
        """ Generate access token """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=120),
                'iat': datetime.utcnow(),
                'iss': 'purwokertodev.github.io',
                'sub': sub
            }

            return jwt.encode(payload, app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode(access_token):
        try:
            payload = jwt.decode(access_token, app.config.get('SECRET_KEY'))
            return payload
        except jwt.ExpiredSignatureError:
            return 'access token expired'
        except jwt.InvalidTokenError:
            return 'access token invalid'