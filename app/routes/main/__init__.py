import asyncio
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.core.db import get_db_session
from app.models import Category, User
from app.utils import role_required
from app import models, crud

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/u/<username>")
@login_required
def get_account(username):
    with get_db_session() as db:
        account = db.query(User).filter_by(username=current_user.username).first()

    return render_template("main/account/index.html", account=account)


@main_bp.route("/")
# @role_required("cashier")
async def index():
    categories, products = await asyncio.gather(
        crud.get_all_categories(True), crud.get_all_products(True)
    )

    return render_template("main/index.html", categories=categories, products=products)


#
# @main_bp.route("/stores/<slug>")
# def detail(slug):
#     with get_db_session() as db:
#         row = db.query(Store).filter_by(is_active=True, slug=slug).first()
#
#     return render_template("main/detail.html", row=row)
#
#
# @main_bp.route("/search")
# def search_store():
#     s = request.args.get("s")
#     category = request.args.get("category")
#     with get_db_session() as db:
#         query = text(f"SELECT * FROM v_search")
#         if s:
#             query = text(f"SELECT * FROM ({query}) as search WHERE name ILIKE '%{s}%'")
#         if category:
#             query = text(
#                 f"SELECT * FROM ({query}) as search WHERE '{category}' = ANY(categories)"
#             )
#         query = text(
#             f"SELECT name, phone, description, open_at, close_at, google_maps, array_to_string(categories, ', ') categories FROM ({query}) search"
#         )
#         rows = db.execute(query)
#
#     return render_template("main/search.html", rows=rows)
