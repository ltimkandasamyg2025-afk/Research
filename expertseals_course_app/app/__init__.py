from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
_db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev-secret-key-change-in-production',
        SQLALCHEMY_DATABASE_URI='sqlite:///courses.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.update(test_config)

    # Initialize extensions with app
    _db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models to register with SQLAlchemy
    from . import models

    with app.app_context():
        _db.create_all()
        # Create default admin user if not exists
        admin_user = models.User.query.filter_by(username='admin').first()
        if not admin_user:
            admin = models.User(username='admin', is_admin=True)
            admin.set_password('admin123')
            _db.session.add(admin)
            _db.session.commit()

    # Register blueprints
    from . import routes, auth, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app

