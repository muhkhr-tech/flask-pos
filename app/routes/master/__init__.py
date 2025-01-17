from flask import Blueprint

master_category_bp = Blueprint(
    "master_category", __name__, template_folder="categories/templates"
)

master_product_bp = Blueprint(
    "master_product", __name__, template_folder="products/templates"
)

master_user_bp = Blueprint("master_user", __name__, template_folder="users/templates")
