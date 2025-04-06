from Module_1.models.user import User


def switch_database(model_name, db_name):
    model_map = {
        "User": User,
    }
    model = model_map.get(model_name)
    if model:
        model.use_db(db_name)
        return f"{model_name} switched to {db_name}."
    return "Model not found"
