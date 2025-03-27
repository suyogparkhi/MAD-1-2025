from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from models import init_db
from models.user import User
import os

# Import controllers
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.user import user_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Configure the application
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "quiz_master.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Initialize the database
    init_db(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    
    # Root route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        return render_template('index.html', title='Welcome to Quiz Master')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 