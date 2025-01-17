from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import current_user

from app.core.db import get_db_session
from app import crud, schemas, models

store_bp = Blueprint("stores", __name__, template_folder="templates")


@store_bp.route("/")
def index():
    with get_db_session() as db:
        rows = db.query(models.Store).filter_by(user_id=current_user.id).all()

    return render_template("stores/index.html", rows=rows)


@store_bp.route("/create", methods=["GET", "POST"])
def create_store():
    if request.method == "POST":
        store = crud.create_store(
            name=request.form["name"],
            categories=request.form.getlist("categories"),
            description=request.form["description"],
            phone=request.form["phone"],
            open_at=request.form["open_at"],
            close_at=request.form["close_at"],
            google_maps=request.form["google_maps"],
            user_id=current_user.id,
        )

        if not store:
            return render_template("stores/create.html")
        crud.create_notification(
            current_app.config["NOTIFICATION_CREATE_STORE"], current_user.id
        )
        return redirect(url_for("stores.index"))
    return render_template("stores/create.html")


@store_bp.route("/<slug>/update", methods=["GET", "POST"])
def update_store(slug):
    with get_db_session() as db:
        store = db.query(models.Store).filter_by(slug=slug).first()
        store_categories = []
        if store.categories:
            store_categories = [
                category.lower() for category in store.categories.split(",")
            ]

    if request.method == "POST":
        store = crud.update_store(
            schemas.StoreUpdate(
                name=request.form["name"],
                categories=request.form.getlist("categories"),
                description=request.form["description"],
                phone=request.form["phone"],
                open_at=request.form["open_at"],
                close_at=request.form["close_at"],
                google_maps=request.form["google_maps"],
                store_id=store.id,
            )
        )

        if not store:
            return render_template(
                "stores/update.html", store=store, store_categories=store_categories
            )

        return redirect(url_for("stores.index"))

    return render_template(
        "stores/update.html", store=store, store_categories=store_categories
    )


@store_bp.route("/<slug>/update-status", methods=["POST"])
def update_status_store(slug):
    crud.update_status_store(slug)
    return redirect(url_for("stores.index"))
