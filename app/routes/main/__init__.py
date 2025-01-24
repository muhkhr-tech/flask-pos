import asyncio
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.core.db import get_db_session
from app.models import Category, User
from app.utils import role_required
from app import models, crud

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
# @login_required
# @role_required("cashier")
async def index():
    get_struct, products = await asyncio.gather(
        crud.get_struct("proses"), crud.get_all_products(True)
    )

    return render_template("main/base.html", sale=get_struct, products=products)
