from app import models
from app.core.db import get_db_session


async def get_all_inventory_logs():
    with get_db_session() as db:
        rows = (
            db.query(models.InventoryLog).order_by(models.InventoryLog.log_date).all()
        )
        return rows
