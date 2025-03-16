from distance_metrics import manhattan_distance, cosine_distance, chebyshev_distance


def with_manhattan_distance(func):
    """
    Декоратор, що змінює функцію відстані на манхеттенську.
    """
    def wrapper(*args, **kwargs):
        kwargs['distance_function'] = manhattan_distance
        return func(*args, **kwargs)
    return wrapper


def with_cosine_distance(func):
    """
    Декоратор, що змінює функцію відстані на косинусну.
    """
    def wrapper(*args, **kwargs):
        kwargs['distance_function'] = cosine_distance
        return func(*args, **kwargs)
    return wrapper


def with_chebyshev_distance(func):
    """
    Декоратор, що змінює функцію відстані на відстань Чебишева.
    """
    def wrapper(*args, **kwargs):
        kwargs['distance_function'] = chebyshev_distance
        return func(*args, **kwargs)
    return wrapper