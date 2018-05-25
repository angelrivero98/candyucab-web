from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY']='a49e3bafcf09f29777bec468ff2cbbe9'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from candyucab import routes
