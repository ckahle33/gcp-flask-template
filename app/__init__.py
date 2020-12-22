from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, logging, pdb

from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config.from_object(Config)
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth = OAuth(app)

from app.errors import blueprint as errors_bp
from app.auth import blueprint as auth_bp

app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp)


from app import routes, models

