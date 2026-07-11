import os
from flask import Flask


def create_app():
    """Application factory — creates and configures the Flask app."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    frontend_dir = os.path.join(base_dir, "..", "FRONTEND")

    app = Flask(
        __name__,
        template_folder=os.path.join(frontend_dir, "templates"),
        static_folder=os.path.join(frontend_dir, "static"),
    )

    # Load configuration from config.py
    app.config.from_object("config")

    # Initialise database and seed data
    from database import init_db
    init_db(app)

    # Register route blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)

    # Register error handlers
    from errors import register_error_handlers
    register_error_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
