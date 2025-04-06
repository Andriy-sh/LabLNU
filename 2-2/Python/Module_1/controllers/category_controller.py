from Module_1.models.category import Category


def create_category(data):
    return Category.create(**data)


def get_category(category_id):
    return Category.get(category_id)
