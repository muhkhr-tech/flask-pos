from flask import flash
from slugify import slugify

from app import schemas, models
from app.core.db import get_db_session
from app.schemas import validate_store_input


def create_store(**data):
    # validate_store_input(
    #     name=data["name"],
    #     categories=data["categories"],
    #     description=data["description"],
    #     phone=data["phone"],
    #     open_at=data["open_at"],
    #     close_at=data["close_at"],
    #     google_maps=data["google_maps"],
    #     user_id=data["user_id"],
    # )

    store = models.Store()

    store.name = data["name"]
    store.slug = slugify(data["name"])
    store.categories = ",".join(data["categories"])
    store.phone = data["phone"]
    store.description = data["description"]
    store.open_at = data["open_at"]
    store.close_at = data["close_at"]
    store.google_maps = data["google_maps"]
    store.user_id = (data["user_id"],)

    with get_db_session() as db:
        try:
            db.add(store)
            db.commit()
            return True
        except:
            flash("Gagal membuat toko.", "error")
            db.rollback()


def update_store(data: schemas.StoreUpdate):
    with get_db_session() as db:
        store = db.query(models.Store).get(data.store_id)

        store.name = data.name
        store.slug = slugify(data.name)
        store.categories = ", ".join(data.categories)
        store.phone = data.phone
        store.description = data.description
        store.open_at = data.open_at
        store.close_at = data.close_at
        store.google_maps = data.google_maps

        try:
            db.commit()
            return True
        except Exception as e:
            flash("Gagal mengubah toko.", "error")


def update_status_store(slug):
    with get_db_session() as db:
        store = db.query(models.Store).filter_by(slug=slug).first()

        store.is_active = not store.is_active
        db.commit()
        db.refresh(store)
