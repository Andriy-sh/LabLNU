from Module_1.models.category import Category
from Module_1.models.product import Product
from controllers.database_controller import *
from route_decorator import handle_request

print("=== Adding user to 'user' DB ===")
User.use_db("user")
print(handle_request("/users/create", data={"name": "Alice", "email": "alice@example.com"}))
print(handle_request("/users/get", user_id=1))

print("\n=== Switching to 'switch_user' DB ===")
print(handle_request("/database/switch", model_name="User", db_name="switch_user"))

print("\n=== Adding user to 'switch_user' DB ===")
print(handle_request("/users/create", data={"name": "Charlie", "email": "charlie@example.com"}))

print("\n=== Retrieving users from different DBs ===")
User.use_db("user")
print("User DB:", handle_request("/users/get", user_id=1))
User.use_db("switch_user")
print("Switch_user DB:", handle_request("/users/get", user_id=1))

print("\n=== Updating user info ===")
print(handle_request("/users/update", user_id=1, data={"name": "Charlie Updated"}))

print("\n=== Adding category to 'category' DB ===")
Category.use_db("category")
print(handle_request("/category/create", data={"name": "Food", "description": "Cheese"}))

print("\n=== Retrieving category by ID ===")
print(handle_request("/category/get", category_id=1))

print("\n=== Adding product to 'product' DB ===")
Product.use_db("product")
print(handle_request("/product/create", data={"name": "Cheese", "price": 100, "quantity": 1, "category_id": 2}))

print("\n=== Retrieving product by ID ===")
print(handle_request("/product/get", product_id=1))

print("\n=== Retrieving products by category_id ===")
print(handle_request("/product/get/by_category_id", category_id=2))
