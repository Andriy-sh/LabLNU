from controllers.user_controller import *
from controllers.database_controller import *

ROUTES = {
    "/users/create": create_user,
    "/users/get": get_user,
    "/users/update": update_user,
    "/users/delete": delete_user,
    "/database/switch": switch_database,
}


def handle_request(path, **kwargs):
    handler = ROUTES.get(path)
    if handler:
        return handler(**kwargs)
    return {"error": "Route not found"}
