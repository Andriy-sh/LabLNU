from distance_metrics import euclidean_distance


def k_nn(X_train, y_train, X_test, k=3, distance_function=euclidean_distance):
    """
    Алгоритм k-найближчих сусідів (k-NN).

    Параметри:
    - X_train: список тренувальних векторів (список списків чисел)
    - y_train: список міток для тренувальних векторів (список чисел)
    - X_test: список тестових векторів (список списків чисел)
    - k: кількість найближчих сусідів (ціле число)
    - distance_function: функція для обчислення відстані (за замовчуванням - евклідова)

    Повертає:
    - Список прогнозованих міток для тестових векторів (список чисел)
    """
    predictions = []
    for test_point in X_test:
        # Обчислити відстані від тестової точки до всіх тренувальних точок
        distances = [(distance_function(test_point, train_point), i)
                     for i, train_point in enumerate(X_train)]
        # Відсортувати за відстанню та вибрати k найближчих
        distances.sort(key=lambda x: x[0])
        k_nearest_indices = [i for _, i in distances[:k]]
        k_nearest_labels = [y_train[i] for i in k_nearest_indices]
        # Вибрати найпоширенішу мітку серед k найближчих
        prediction = max(set(k_nearest_labels), key=k_nearest_labels.count)
        predictions.append(prediction)
    return predictions