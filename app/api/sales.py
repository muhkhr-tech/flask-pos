import json

from flask import request, jsonify
from flask_login import current_user

from . import api_bp
from app import crud, models


@api_bp.route("/sales", methods=["POST"])
async def create_sale():
    user_id = current_user.user_id
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    product_id = data.get("product_id")
    price = data.get("price")

    get_sale_await = await crud.get_sale("menunggu")

    if get_sale_await:
        if await crud.update_sale(user_id, get_sale_await.sale_id, product_id, price):
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Struk berhasil diubah.",
                        "user_id": user_id,
                        "product_id": product_id,
                        "price": price,
                    }
                ),
                200,
            )

        return jsonify({"status": "error", "message": "Struk gagal diubah."}), 500

    if await crud.create_sale(user_id, product_id, price):
        return (
            jsonify(
                {
                    "message": "Struk baru berhasil ditambah.",
                    "user_id": user_id,
                    "product_id": product_id,
                    "price": price,
                }
            ),
            201,
        )

    return jsonify({"status": "error", "message": "Gagal membuat struk."}), 500
