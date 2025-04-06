from Module_1.controllers.category_controller import *
from Module_1.controllers.product_controller import *
from controllers.user_controller import *
from controllers.database_controller import *

ROUTES = {
    "/users/create": create_user,
    "/users/get": get_user,
    "/users/update": update_user,
    "/users/delete": delete_user,
    "/database/switch": switch_database,
    "/product/create": create_product,
    "/product/get": get_product,
    "/product/get/by_category_id": get_product_by_category_id,
    "/category/create": create_category,
    "/category/get": get_category,
}


def handle_request(path, **kwargs):
    handler = ROUTES.get(path)
    if handler:
        return handler(**kwargs)
    return {"error": "Route not found"}
