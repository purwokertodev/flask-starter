from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from src.server.server import db
from src.user.domain.user import User
from src.shared.jwt_util import JwtUtil

USER_BLUEPRINT = Blueprint('user', __name__)

class RegisterAPI(MethodView):
    """ Register resource """
    def post(self):

        # get data from body
        json_data = request.get_json()

        user = User.query.filter_by(email=json_data.get('email')).first()
        if not user:
            try:
                user = User(name=json_data.get('name'), email=json_data.get('email'), password=json_data.get('password'))
                db.session.add(user)
                db.session.commit()

                resp = {
                    'success': True,
                    'message': 'register user',
                    'data': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'password': user.password
                    }
                }

                return make_response(jsonify(resp)), 201
            except Exception as e:
                resp = {
                    'success': False,
                    'message': 'error occured',
                    'data': {}
                }

                return make_response(jsonify(resp)), 400
        else:
            resp = {
                    'success': False,
                    'message': 'user already exist',
                    'data': {}
                }

            return make_response(jsonify(resp)), 400

class LoginAPI(MethodView):
    """ Login resource """
    def post(self):
         # get data from body
        json_data = request.get_json()

        try:
            user = User.query.filter_by(email=json_data.get('email')).first()
            if user:
                if not user.is_valid_password(json_data.get('password')):
                    resp = {
                        'success': False,
                        'message': 'invalid username or password',
                        'data': {}
                    }

                    return make_response(jsonify(resp)), 401
                
                access_token = JwtUtil.encode(sub=user.id)
                if access_token:
                    resp = {
                        'success': True,
                        'message': 'login success',
                        'data': {
                            'access_token': access_token.decode()
                        }
                    }

                    return make_response(jsonify(resp)), 200
            else:
                resp = {
                        'success': False,
                        'message': 'invalid username or password',
                        'data': {}
                    }

                return make_response(jsonify(resp)), 401
        except:
            resp = {
                        'success': False,
                        'message': 'invalid username or password',
                        'data': {}
                    }

            return make_response(jsonify(resp)), 401

class MeAPI(MethodView):
    """ Me resource """
    def get(self):
        
        # get authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_jwt = auth_header.split(' ')[1]
            except IndexError:
                resp = {
                        'success': False,
                        'message': 'invalid authorization header',
                        'data': {}
                    }

                return make_response(jsonify(resp)), 401
        else:
            auth_jwt = ''

        if auth_jwt:
            token = JwtUtil.decode(auth_jwt)
            if not isinstance(token, str):
                user = User.query.filter_by(id=token['sub']).first()
                resp = {
                    'success': True,
                    'message': 'get me',
                    'data': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'password': user.password
                    }
                }

                return make_response(jsonify(resp)), 200

            resp = {
                        'success': False,
                        'message': 'invalid authorization header',
                        'data': {}
                    }

            return make_response(jsonify(resp)), 401
        else:
            resp = {
                        'success': False,
                        'message': 'invalid authorization header',
                        'data': {}
                    }

            return make_response(jsonify(resp)), 401

register_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
me_view = MeAPI.as_view('me_api')

USER_BLUEPRINT.add_url_rule('/users', view_func=register_view, methods=['POST'])
USER_BLUEPRINT.add_url_rule('/auth', view_func=login_view, methods=['POST'])
USER_BLUEPRINT.add_url_rule('/me', view_func=me_view, methods=['GET'])

