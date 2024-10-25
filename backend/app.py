from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS  
from .app_config import Config
from .db import db

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load configuration from your app config
    app.config.from_object(Config)

    # Initialize the database and migration handling
    db.init_app(app)
    migrate = Migrate(app, db)  # Flask-Migrate for handling migrations

    # Enable CORS for all routes
    CORS(app)

    # Register your routes
    with app.app_context():
        from .routes import chat_bp
        app.register_blueprint(chat_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    # Start the Flask application
    app.run(debug=True)
