import random
from vector_operations import vector_mean, vector_subtract, vector_norm
from distance_metrics import euclidean_distance


def k_means(X, k=3, max_iters=100, tol=1e-4, distance_function=euclidean_distance):
    """
    Алгоритм k-середніх (k-means).

    Параметри:
    - X: список векторів (список списків чисел)
    - k: кількість кластерів (ціле число)
    - max_iters: максимальна кількість ітерацій (ціле число)
    - tol: поріг збіжності (число)
    - distance_function: функція для обчислення відстані (за замовчуванням - евклідова)

    Повертає:
    - labels: список міток кластерів для кожного вектора (список чисел)
    - centers: список центрів кластерів (список списків чисел)
    """
    # Ініціалізація центрів випадковим чином
    centers = random.sample(X, k)
    labels = [0] * len(X)

    for iteration in range(max_iters):
        # Призначення точок до кластерів
        new_labels = []
        for point in X:
            distances = [distance_function(point, center) for center in centers]
            new_label = distances.index(min(distances))
            new_labels.append(new_label)

        # Перевірка на збіжність
        if new_labels == labels:
            break
        labels = new_labels

        # Оновлення центрів
        new_centers = []
        for cluster_idx in range(k):
            cluster_points = [X[i] for i, label in enumerate(labels) if label == cluster_idx]
            if cluster_points:
                new_centers.append(vector_mean(cluster_points))
            else:
                new_centers.append(centers[cluster_idx])

        # Перевірка на збіжність за зміною центрів
        center_shift = sum(vector_norm(vector_subtract(new_centers[i], centers[i])) for i in range(k))
        if center_shift < tol:
            break
        centers = new_centers

    return labels, centers