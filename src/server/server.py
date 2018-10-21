from flask import Flask
import markdown
import os

from src.foo.domain.foo import Foo

# create instance of Flask
app = Flask(__name__)

@app.route("/")
def index():
	"""this is index route"""
	# i use this to open Readme.file :D
	with open(os.getcwd() + '/Readme.md', 'r') as readme_file:
		content = readme_file.read()
		return markdown.markdown(content)

@app.route("/hello")
def hello():
	"""-,-"""
	f = Foo("Wury", "wuriyanto48@yahoo.co.id", "12345")
	print(f.is_valid_password("12345"))
	return f.display()