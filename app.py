from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from extension import db
from models import User
from routes import api
import os

app = Flask(__name__)

# Configure app
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'api.login'

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)