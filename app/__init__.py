from flask import Flask
from config import Config

# Extensions will be initialized here later
# db = SQLAlchemy()
# migrate = Migrate()
# login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize plugins
    # db.init_app(app)
    # migrate.init_app(app, db)
    # login_manager.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.crm import bp as crm_bp
    app.register_blueprint(crm_bp, url_prefix='/crm')

    return app
