from flask import Flask, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import markdown
import os



# create instance of Flask
app = Flask(__name__)
CORS(app)

app_env = os.getenv('APP_ENV', 'config.env.DevelopmentConfig')

app.config.from_object(app_env)

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

@app.route("/")
def index():
	"""this is index route"""
	# i use this to open Readme.file :D
	with open(os.getcwd() + '/Readme.md', 'r') as readme_file:
		content = readme_file.read()
		return markdown.markdown(content)

from src.user.delivery.flask_handler import USER_BLUEPRINT
app.register_blueprint(USER_BLUEPRINT)