from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

from models import db, bcrypt
from resources.auth import Register, Login
from resources.notes import Notes, NoteById

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# Init extensions
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app)

# Register routes
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Notes, "/notes")
api.add_resource(NoteById, "/notes/<int:id>")

# IMPORTANT: ensures models are registered
import models

if __name__ == "__main__":
    app.run(debug=True)