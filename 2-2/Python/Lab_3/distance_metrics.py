import math
from vector_operations import dot_product, vector_norm


def euclidean_distance(x, y):
    """
    Обчислює евклідову відстань між двома векторами.

    Параметри:
    - x: перший вектор (список чисел)
    - y: другий вектор (список чисел)

    Повертає:
    - Евклідова відстань (число)
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))


def manhattan_distance(x, y):
    """
    Обчислює манхеттенську відстань між двома векторами.

    Параметри:
    - x: перший вектор (список чисел)
    - y: другий вектор (список чисел)

    Повертає:
    - Манхеттенська відстань (число)
    """
    return sum(abs(a - b) for a, b in zip(x, y))


def cosine_distance(x, y):
    """
    Обчислює косинусну відстань між двома векторами.

    Параметри:
    - x: перший вектор (список чисел)
    - y: другий вектор (список чисел)

    Повертає:
    - Косинусна відстань (число)
    """
    dot = dot_product(x, y)
    norm_x = vector_norm(x)
    norm_y = vector_norm(y)
    return 1 - (dot / (norm_x * norm_y)) if norm_x * norm_y > 0 else 1


def chebyshev_distance(x, y):
    """
    Обчислює відстань Чебишева між двома векторами.

    Параметри:
    - x: перший вектор (список чисел)
    - y: другий вектор (список чисел)

    Повертає:
    - Відстань Чебишева (число)
    """
    return max(abs(a - b) for a, b in zip(x, y))
