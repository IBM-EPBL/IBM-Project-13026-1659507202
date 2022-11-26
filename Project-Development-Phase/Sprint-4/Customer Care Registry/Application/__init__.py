from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='./Templates')
app.secret_key = "668413f3d48637a7355c99c18db4e60a604cb917d5c4dcd7"
CORS(app)

from Application import database

from Application import models

from Application import routes
