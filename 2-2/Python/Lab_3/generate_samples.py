import math
import random
import pickle
import os


def generate_classification_data(n_samples=100, n_test=20, n_features=2, seed=42):
    """
    Generates data for a classification task (for k-NN).

    Parameters:
    - n_samples: number of training samples
    - n_test: number of test samples
    - n_features: number of features
    - seed: random number generator seed

    Returns:
    - X_train: list of training samples
    - y_train: list of class labels for training samples
    - X_test: list of test samples
    - y_test: list of true labels for test samples
    """
    random.seed(seed)

    # Class centers
    centers = [
        [random.uniform(-5, 5) for _ in range(n_features)],  # First class center
        [random.uniform(-5, 5) for _ in range(n_features)]  # Second class center
    ]

    # Generate training data
    X_train = []
    y_train = []

    for _ in range(n_samples):
        # Choose a random class (0 or 1)
        class_idx = random.randint(0, 1)

        # Generate a point around the class center
        point = []
        for j in range(n_features):
            # Add random offset from the center
            value = centers[class_idx][j] + random.gauss(0, 1.5)
            point.append(value)

        X_train.append(point)
        y_train.append(class_idx)

    # Generate test data
    X_test = []
    y_test = []

    for _ in range(n_test):
        class_idx = random.randint(0, 1)

        point = []
        for j in range(n_features):
            value = centers[class_idx][j] + random.gauss(0, 1.5)
            point.append(value)

        X_test.append(point)
        y_test.append(class_idx)

    return X_train, y_train, X_test, y_test


def generate_multiclass_data(n_samples=100, n_test=20, n_features=2, n_classes=3, seed=42):
    """
    Generates data for multiclass classification.

    Parameters:
    - n_samples: number of training samples
    - n_test: number of test samples
    - n_features: number of features
    - n_classes: number of classes
    - seed: random number generator seed

    Returns:
    - X_train: list of training samples
    - y_train: list of class labels for training samples
    - X_test: list of test samples
    - y_test: list of true labels for test samples
    """
    random.seed(seed)

    # Class centers
    centers = []
    for _ in range(n_classes):
        center = [random.uniform(-8, 8) for _ in range(n_features)]
        centers.append(center)

    # Generate training data
    X_train = []
    y_train = []

    samples_per_class = n_samples // n_classes
    for class_idx in range(n_classes):
        for _ in range(samples_per_class):
            point = []
            for j in range(n_features):
                value = centers[class_idx][j] + random.gauss(0, 1.0)
                point.append(value)

            X_train.append(point)
            y_train.append(class_idx)

    # Generate test data
    X_test = []
    y_test = []

    tests_per_class = n_test // n_classes
    for class_idx in range(n_classes):
        for _ in range(tests_per_class):
            point = []
            for j in range(n_features):
                value = centers[class_idx][j] + random.gauss(0, 1.0)
                point.append(value)

            X_test.append(point)
            y_test.append(class_idx)

    return X_train, y_train, X_test, y_test


def generate_clustering_data(n_points=300, n_clusters=3, n_features=2, seed=42):
    """
    Generates data for a clustering task (for k-means).

    Parameters:
    - n_points: total number of points
    - n_clusters: number of clusters
    - n_features: number of features
    - seed: random number generator seed

    Returns:
    - X: list of data points
    - true_labels: list of true cluster labels (for quality evaluation)
    """
    random.seed(seed)

    # Cluster centers
    centers = []
    for _ in range(n_clusters):
        center = [random.uniform(-10, 10) for _ in range(n_features)]
        centers.append(center)

    # Generate data points
    X = []
    true_labels = []

    points_per_cluster = n_points // n_clusters
    for cluster_idx in range(n_clusters):
        for _ in range(points_per_cluster):
            point = []
            for j in range(n_features):
                # Add random offset from the cluster center
                value = centers[cluster_idx][j] + random.gauss(0, 2.0)
                point.append(value)

            X.append(point)
            true_labels.append(cluster_idx)

    return X, true_labels


def generate_noisy_data(n_points=100, n_features=2, noise_level=1.0, seed=42):
    """
    Generates noisy data without a clear cluster structure.

    Parameters:
    - n_points: number of points
    - n_features: number of features
    - noise_level: noise level
    - seed: random number generator seed

    Returns:
    - X: list of data points
    """
    random.seed(seed)

    X = []
    for _ in range(n_points):
        point = [random.gauss(0, noise_level) for _ in range(n_features)]
        X.append(point)

    return X


def generate_nonlinear_data(n_points=200, seed=42):
    """
    Generates nonlinearly separable data (e.g., concentric circles).

    Parameters:
    - n_points: number of points
    - seed: random number generator seed

    Returns:
    - X: list of data points
    - y: list of class labels
    """
    random.seed(seed)

    X = []
    y = []

    # First class - inner circle
    inner_points = n_points // 2
    for _ in range(inner_points):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 3)
        x = radius * math.cos(angle)
        y_coord = radius * math.sin(angle)

        X.append([x, y_coord])
        y.append(0)

    # Second class - outer ring
    outer_points = n_points - inner_points
    for _ in range(outer_points):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(5, 8)
        x = radius * math.cos(angle)
        y_coord = radius * math.sin(angle)

        X.append([x, y_coord])
        y.append(1)

    return X, y


def save_data(data, filename):
    """
    Saves data to a file using pickle.

    Parameters:
    - data: the data to save
    - filename: the name of the file
    """
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print(f"Data saved to {filename}")


def load_data(filename):
    """
    Loads data from a file using pickle.

    Parameters:
    - filename: the name of the file

    Returns:
    - the loaded data
    """
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(f"Data loaded from {filename}")
    return data


if __name__ == "__main__":
    # Create a directory for the data files
    os.makedirs("data", exist_ok=True)

    # Generate classification data
    X_train, y_train, X_test, y_test = generate_classification_data(n_samples=100, n_test=20)
    print(f"Generated {len(X_train)} training samples and {len(X_test)} test samples for classification")
    print(f"Example training sample: {X_train[0]}, class: {y_train[0]}")

    # Save classification data
    save_data((X_train, y_train, X_test, y_test), "data/classification_data.pkl")

    # Generate multiclass classification data
    X_multi_train, y_multi_train, X_multi_test, y_multi_test = generate_multiclass_data(n_classes=4)
    print(f"\nGenerated data for classification with {len(set(y_multi_train))} classes")

    # Save multiclass data
    save_data((X_multi_train, y_multi_train, X_multi_test, y_multi_test), "data/multiclass_data.pkl")

    # Generate clustering data
    X_cluster, true_labels = generate_clustering_data(n_points=300, n_clusters=3)
    print(f"\nGenerated {len(X_cluster)} points for clustering with {len(set(true_labels))} true clusters")

    # Save clustering data
    save_data((X_cluster, true_labels), "data/clustering_data.pkl")

    # Generate noisy data
    X_noisy = generate_noisy_data(n_points=50)
    print(f"\nGenerated {len(X_noisy)} noisy points")

    # Save noisy data
    save_data(X_noisy, "data/noisy_data.pkl")

    # Generate nonlinear data
    X_nonlinear, y_nonlinear = generate_nonlinear_data(n_points=200)
    print(f"\nGenerated {len(X_nonlinear)} points with nonlinear separation")

    # Save nonlinear data
    save_data((X_nonlinear, y_nonlinear), "data/nonlinear_data.pkl")

    # Example of loading data back
    print("\n--- Loading data examples ---")
    loaded_classification_data = load_data("data/classification_data.pkl")
    loaded_X_train, loaded_y_train, loaded_X_test, loaded_y_test = loaded_classification_data
    print(f"Loaded classification data: {len(loaded_X_train)} training samples, {len(loaded_X_test)} test samples")

    loaded_multiclass_data = load_data("data/multiclass_data.pkl")
    loaded_X_multi_train, loaded_y_multi_train, loaded_X_multi_test, loaded_y_multi_test = loaded_multiclass_data
    print(
        f"Loaded multiclass data: {len(loaded_X_multi_train)} training samples with {len(set(loaded_y_multi_train))} classes")

    loaded_clustering_data = load_data("data/clustering_data.pkl")
    loaded_X_cluster, loaded_true_labels = loaded_clustering_data
    print(f"Loaded clustering data: {len(loaded_X_cluster)} points with {len(set(loaded_true_labels))} clusters")

    loaded_X_noisy = load_data("data/noisy_data.pkl")
    print(f"Loaded noisy data: {len(loaded_X_noisy)} points")

    loaded_nonlinear_data = load_data("data/nonlinear_data.pkl")
    loaded_X_nonlinear, loaded_y_nonlinear = loaded_nonlinear_data
    print(f"Loaded nonlinear data: {len(loaded_X_nonlinear)} points")
