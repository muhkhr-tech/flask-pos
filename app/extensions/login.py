from flask_login import LoginManager

from app.core.db import get_db_session
from app.models import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    with get_db_session() as db:
        return db.query(User).get(user_id)
