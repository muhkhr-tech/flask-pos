from flask import Flask


def create_app(config_name):
    from app.config import config
    from .routes import (
        main_bp,
        master_category_bp,
        master_product_bp,
        master_user_bp,
        auth_bp,
        sale_bp,
    )
    from .api import api_bp

    from .extensions import bcrypt, csrf, login_manager

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(master_category_bp, url_prefix="/master/categories")
    app.register_blueprint(master_product_bp, url_prefix="/master/products")
    app.register_blueprint(sale_bp, url_prefix="/sales")
    app.register_blueprint(master_user_bp, url_prefix="/master/users")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
