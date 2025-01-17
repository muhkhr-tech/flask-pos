from flask import render_template
from flask_login import login_required

from app.core.db import get_db_session
from app.models import User
from app.routes.master import master_user_bp


@master_user_bp.route("/")
@login_required
def index():
    with get_db_session() as db:
        rows = db.query(User).all()

    return render_template("users/index.html", rows=rows)
