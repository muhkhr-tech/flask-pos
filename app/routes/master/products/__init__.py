import logging
from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required
from slugify import slugify

from app.core.db import get_db_session
from app.models import Product
from app import crud
from app.routes.master import master_product_bp


@master_product_bp.route("/")
@login_required
def index():
    with get_db_session() as db:
        rows = db.query(Product).all()

    return render_template("products/index.html", rows=rows)


@master_product_bp.route("/create", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        if crud.create_product(request.form["name"], request.form["price"]):
            return redirect(url_for("master_product.index"))
    return render_template("products/create.html")


@master_product_bp.route("/<id>/update-stock", methods=["GET", "POST"])
def update_stock_product(id):

    if request.method == "POST":
        if crud.update_stock_product(id, request.form["stock"]):
            return redirect(url_for("master_product.index"))

    return render_template("products/update-stock.html", product=None)


@master_product_bp.route("/<id>/update-status", methods=["POST"])
def update_status_product(id):
    crud.update_status_product(id)
    return redirect(url_for("master_product.index"))
