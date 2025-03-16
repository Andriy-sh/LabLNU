from knn import k_nn
from kmeans import k_means
from decorators import with_manhattan_distance, with_cosine_distance, with_chebyshev_distance
import matplotlib.pyplot as plt
from generate_samples import load_data

# Приклад даних для класифікації
X_train = [[1, 2], [2, 3], [3, 3], [6, 7], [7, 8], [8, 8], [10, 2], [11, 3], [12, 4]]
y_train = [0, 0, 0, 1, 1, 1, 2, 2, 2]  # Додано третій клас
X_test = [[4, 4], [5, 5], [9, 3], [10, 4],[8,8]]  # Додано більше тестових точок

# Приклад даних для кластеризації
X_cluster = [[1, 2], [2, 3], [3, 3], [6, 7], [7, 8], [8, 8], [10, 2], [11, 3], [12, 4]]

# X_train, y_train, X_test, y_test = load_data("data/classification_data.pkl")
# X_cluster, true_labels = load_data("data/clustering_data.pkl")

# Тестування k-NN з різними метриками
print("k-NN з евклідовою відстанню:", k_nn(X_train, y_train, X_test))
print("k-NN з манхеттенською відстанню:", with_manhattan_distance(k_nn)(X_train, y_train, X_test))
print("k-NN з косинусною відстанню:", with_cosine_distance(k_nn)(X_train, y_train, X_test))
print("k-NN з відстанню Чебишева:", with_chebyshev_distance(k_nn)(X_train, y_train, X_test))

# Тестування k-means з різними метриками
labels, centers = k_means(X_cluster, k=3)
print("k-means з евклідовою відстанню:", labels, centers)
labels, centers = with_manhattan_distance(k_means)(X_cluster, k=3)
print("k-means з манхеттенською відстанню:", labels, centers)

# Візуалізація результатів k-NN
def plot_knn_results(X_train, y_train, X_test, y_pred, title):
    plt.figure(figsize=(10, 6))
    # Візуалізація тренувальних даних
    colors = ['blue', 'red', 'green']
    for i, class_label in enumerate(set(y_train)):
        class_points = [X_train[j] for j in range(len(X_train)) if y_train[j] == class_label]
        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]
        plt.scatter(x_coords, y_coords, color=colors[i], label=f'Class {class_label} (train)', alpha=0.6)
    # Візуалізація тестових даних
    for i, class_label in enumerate(set(y_pred)):
        class_points = [X_test[j] for j in range(len(X_test)) if y_pred[j] == class_label]
        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]
        plt.scatter(x_coords, y_coords, color=colors[class_label], marker='x', s=100, label=f'Class {class_label} (test)')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Візуалізація результатів k-means
def plot_kmeans_results(X, labels, centers, title):
    plt.figure(figsize=(10, 6))
    colors = ['blue', 'red', 'green']
    for i, cluster_label in enumerate(set(labels)):
        cluster_points = [X[j] for j in range(len(X)) if labels[j] == cluster_label]
        x_coords = [point[0] for point in cluster_points]
        y_coords = [point[1] for point in cluster_points]
        plt.scatter(x_coords, y_coords, color=colors[i], label=f'Cluster {cluster_label}', alpha=0.6)
    # Візуалізація центрів кластерів
    center_x = [center[0] for center in centers]
    center_y = [center[1] for center in centers]
    plt.scatter(center_x, center_y, color='black', marker='X', s=200, label='Centers')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Візуалізація k-NN з різними метриками
y_pred_euclidean = k_nn(X_train, y_train, X_test)
plot_knn_results(X_train, y_train, X_test, y_pred_euclidean, "k-NN з евклідовою відстанню")

y_pred_manhattan = with_manhattan_distance(k_nn)(X_train, y_train, X_test)
plot_knn_results(X_train, y_train, X_test, y_pred_manhattan, "k-NN з манхеттенською відстанню")

y_pred_cosine = with_cosine_distance(k_nn)(X_train, y_train, X_test)
plot_knn_results(X_train, y_train, X_test, y_pred_cosine, "k-NN з косинусною відстанню")

y_pred_chebyshev = with_chebyshev_distance(k_nn)(X_train, y_train, X_test)
plot_knn_results(X_train, y_train, X_test, y_pred_chebyshev, "k-NN з відстанню Чебишева")

# Візуалізація k-means з різними метриками
labels_euclidean, centers_euclidean = k_means(X_cluster, k=3)
plot_kmeans_results(X_cluster, labels_euclidean, centers_euclidean, "k-means з евклідовою відстанню")

labels_manhattan, centers_manhattan = with_manhattan_distance(k_means)(X_cluster, k=3)
plot_kmeans_results(X_cluster, labels_manhattan, centers_manhattan, "k-means з манхеттенською відстанню")