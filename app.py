import os
from flask import Flask, render_template
from config import Config
from database.db import close_db, init_db

def create_app(config_class=Config):
    """Application Factory Pattern for RideShare."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register teardown function to clean up database connections
    app.teardown_appcontext(close_db)

    # Register Blueprints
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.rider_routes import rider_bp
    from routes.driver_routes import driver_bp
    from routes.admin_routes import admin_bp
    from routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(rider_bp)
    app.register_blueprint(driver_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Global Error Handlers (Section 14: Friendly Error Handling)
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    # Initialize SQLite database & seed demo accounts if new
    init_db(app)

    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print(" 🚗 RideShare - Ride Sharing Web Application")
    print(" Running on http://127.0.0.1:5000")
    print(" Demo Accounts:")
    print("   • Rider:  rider@demo.com  / Rider@123")
    print("   • Driver: driver@demo.com / Driver@123")
    print("   • Admin:  admin@demo.com  / Admin@123")
    print("="*60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
