from flask import Blueprint, jsonify

from app.core.db import get_db_session
from app import models

api_bp = Blueprint("api", __name__)

from .sales import *


@api_bp.route("/notifications/<int:user_id>/")
def get_notifications(user_id):
    with get_db_session() as db:
        notifications = (
            db.query(models.Notification)
            .filter_by(user_id=user_id)
            .order_by(models.Notification.created_at.desc())
            .all()
        )

    return jsonify(
        {
            "status": "success",
            "message": "Berhasil mengambil data",
            "data": [
                {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "is_read": notification.is_read,
                    "created_at": notification.created_at,
                }
                for notification in notifications
            ],
        }
    )


@api_bp.route("/notifications/<int:notification_id>/set-status-read")
def set_status_to_read(notification_id):
    with get_db_session() as db:
        notification = db.query(models.Notification).get(notification_id)
        notification.is_read = True
        db.commit()

    return jsonify(
        {"status": "success", "message": "Berhasil mengubah status", "data": None}
    )
