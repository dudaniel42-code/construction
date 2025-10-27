from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
import os

app = Flask(__name__, template_folder='templates')  # Change to 'templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plans.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your-secret-key'

# Create folders if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.template_folder, exist_ok=True)

db.init_app(app)

def register_blueprints():
    from routes.main import create_main_blueprint
    from routes.admin import create_admin_blueprint
    main = create_main_blueprint()
    admin = create_admin_blueprint()
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

with app.app_context():
    db.create_all()
    register_blueprints()

if __name__ == '__main__':
    app.run(debug=True)