from Module_1.models.user import User

def create_user(data):
    return User.create(**data)

def get_user(user_id):
    return User.get(user_id)

def update_user(user_id, data):
    return User.update(user_id, **data)

def delete_user(user_id):
    return User.delete(user_id)
