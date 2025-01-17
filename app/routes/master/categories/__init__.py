import logging
from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required
from slugify import slugify

from app.core.db import get_db_session
from app.models import Category
from app import crud
from app.routes.master import master_category_bp


@master_category_bp.route("/")
def index():
    with get_db_session() as db:
        rows = db.query(Category).all()

    return render_template("categories/index.html", rows=rows)


@master_category_bp.route("/create", methods=["GET", "POST"])
def create_category():
    if request.method == "POST":
        if crud.create_category(
            request.form["code"], request.form["name"], request.form["description"]
        ):
            return redirect(url_for("master_category.index"))
    return render_template("categories/create.html")


@master_category_bp.route("/<id>/update-status", methods=["POST"])
def update_status_category(id):
    crud.categories.update_status_category(id)
    return redirect(url_for("master_category.index"))
