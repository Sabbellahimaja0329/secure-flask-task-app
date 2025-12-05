# app/__init__.py
import os
from flask import Flask, session, render_template
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from datetime import datetime

load_dotenv()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # existing config...
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE','False') == 'True'

    csrf.init_app(app)

    # register blueprints...
    from .auth import auth_bp
    from .tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}

    @app.route('/')
    def index():
        """
        Always render the home landing page.
        If a user is logged in, the template will show a quick access panel.
        """
        return render_template('home.html')

    return app