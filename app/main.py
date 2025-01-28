from flask import Flask, g, request, url_for, redirect

from app.core.db import get_db_session


def create_app(config_name):
    from app.config import config
    from .routes import (
        main_bp,
        master_category_bp,
        master_product_bp,
        master_user_bp,
        auth_bp,
        sale_bp,
        start_bp,
    )

    from .extensions import bcrypt, csrf, login_manager
    from app import models

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
    app.register_blueprint(start_bp, url_prefix="/starts")

    @app.before_request
    def check_existing_admin():
        if not hasattr(g, "admin_exists"):
            with get_db_session() as db:
                g.admin_exists = (
                    db.query(models.User).filter_by(role="admin").first() is not None
                )

        if not g.admin_exists:
            if (
                request.endpoint != "starts.create_admin"
                and not request.path.startswith("/static")
            ):
                return redirect(url_for("starts.create_admin"))

        print(request.path)

    return app
