import matplotlib.pyplot as plt
import pickle
from matplotlib.colors import ListedColormap


def visualize_classification_results(X_train, y_train, X_test, y_test, y_pred, title="Classification Results"):
    """
    Visualizes classification data including both true labels and predictions.

    Parameters:
    - X_train: list of training feature vectors (2D)
    - y_train: list of training labels
    - X_test: list of test feature vectors
    - y_test: list of true test labels
    - y_pred: list of predicted labels for test data
    - title: plot title
    """
    # Check if the data is 2D (for visualization)
    if len(X_train[0]) != 2:
        print("Error: Can only visualize 2D data. Your data has", len(X_train[0]), "dimensions.")
        return

    plt.figure(figsize=(15, 6))

    # Get unique classes
    unique_classes = sorted(list(set(y_train)))
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

    # Plot 1: Training and test data with true labels
    plt.subplot(1, 2, 1)

    # Plot training data
    for i, class_label in enumerate(unique_classes):
        indices = [j for j, label in enumerate(y_train) if label == class_label]
        class_points = [X_train[j] for j in indices]

        # Extract coordinates
        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]

        # Plot this class
        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'Class {class_label} (train)',
                    marker='o', alpha=0.3)

    # Plot test data with true labels
    for i, class_label in enumerate(unique_classes):
        indices = [j for j, label in enumerate(y_test) if label == class_label]
        class_points = [X_test[j] for j in indices]

        if not class_points:  # Skip if no points for this class
            continue

        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'Class {class_label} (test)',
                    marker='s', alpha=0.7, s=80)

    plt.title(f"{title} - True Labels")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Test data with predicted labels
    plt.subplot(1, 2, 2)

    # Plot training data (muted)
    for i, class_label in enumerate(unique_classes):
        indices = [j for j, label in enumerate(y_train) if label == class_label]
        class_points = [X_train[j] for j in indices]

        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, alpha=0.1)  # Very transparent

    # Plot test data with predicted labels
    for i, class_label in enumerate(unique_classes):
        indices = [j for j, pred in enumerate(y_pred) if pred == class_label]
        class_points = [X_test[j] for j in indices]

        if not class_points:  # Skip if no predictions for this class
            continue

        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'Predicted Class {class_label}',
                    marker='x', alpha=1.0, s=100)

    # Highlight misclassified points
    misclassified_indices = [i for i in range(len(y_test)) if y_test[i] != y_pred[i]]

    if misclassified_indices:
        misclassified_points = [X_test[i] for i in misclassified_indices]
        x_coords = [point[0] for point in misclassified_points]
        y_coords = [point[1] for point in misclassified_points]

        plt.scatter(x_coords, y_coords, color='black', label='Misclassified',
                    marker='o', facecolors='none', s=150, linewidth=2)

    plt.title(f"{title} - Predicted Labels")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add accuracy information
    accuracy = sum(1 for i in range(len(y_test)) if y_test[i] == y_pred[i]) / len(y_test)
    plt.figtext(0.5, 0.01, f'Accuracy: {accuracy:.2%}', ha='center', fontsize=12,
                bbox=dict(facecolor='yellow', alpha=0.5))

    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")
    plt.show()

    return accuracy


def visualize_clustering_comparison(X, true_labels, predicted_labels, centers=None, title="Clustering Comparison"):
    """
    Visualizes clustering results comparing true and predicted clusters.

    Parameters:
    - X: list of data points (2D)
    - true_labels: list of true cluster labels
    - predicted_labels: list of predicted cluster labels
    - centers: list of predicted cluster centers (optional)
    - title: plot title
    """
    # Check if the data is 2D
    if len(X[0]) != 2:
        print("Error: Can only visualize 2D data. Your data has", len(X[0]), "dimensions.")
        return

    plt.figure(figsize=(15, 6))

    # Colors for clusters
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

    # Plot 1: True clusters
    plt.subplot(1, 2, 1)

    unique_true_labels = sorted(list(set(true_labels)))
    for i, label in enumerate(unique_true_labels):
        indices = [j for j, l in enumerate(true_labels) if l == label]
        cluster_points = [X[j] for j in indices]

        x_coords = [point[0] for point in cluster_points]
        y_coords = [point[1] for point in cluster_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'True Cluster {label}', alpha=0.7)

    plt.title(f"{title} - True Clusters")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Predicted clusters
    plt.subplot(1, 2, 2)

    unique_pred_labels = sorted(list(set(predicted_labels)))
    for i, label in enumerate(unique_pred_labels):
        indices = [j for j, l in enumerate(predicted_labels) if l == label]
        cluster_points = [X[j] for j in indices]

        x_coords = [point[0] for point in cluster_points]
        y_coords = [point[1] for point in cluster_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'Predicted Cluster {label}', alpha=0.7)

    # Add centers if provided
    if centers:
        center_x = [center[0] for center in centers]
        center_y = [center[1] for center in centers]
        plt.scatter(center_x, center_y, color='black', marker='X', s=200, label='Cluster Centers')

    plt.title(f"{title} - Predicted Clusters")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Calculate and display clustering agreement
    # (This is a simplified measure and not as sophisticated as measures like adjusted Rand index)
    agreement_score = calculate_cluster_agreement(true_labels, predicted_labels)
    plt.figtext(0.5, 0.01, f'Cluster Agreement Score: {agreement_score:.2f}', ha='center',
                fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5))

    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")
    plt.show()

    return agreement_score


def calculate_cluster_agreement(true_labels, predicted_labels):
    """
    Calculates a simple cluster agreement score between true and predicted clusters.
    This is a simplified metric and not as sophisticated as measures like adjusted Rand index.

    The score ranges from 0 to 1, where 1 means perfect agreement.
    """
    # Create pairs of points
    n = len(true_labels)
    pairs_same_true = set()
    pairs_same_pred = set()

    for i in range(n):
        for j in range(i + 1, n):
            # If two points are in the same cluster in true labels
            if true_labels[i] == true_labels[j]:
                pairs_same_true.add((i, j))

            # If two points are in the same cluster in predicted labels
            if predicted_labels[i] == predicted_labels[j]:
                pairs_same_pred.add((i, j))

    # Calculate agreement
    intersection = len(pairs_same_true.intersection(pairs_same_pred))
    union = len(pairs_same_true.union(pairs_same_pred))

    if union == 0:  # Handle edge case
        return 1.0

    return intersection / union


def visualize_decision_boundaries(X_train, y_train, X_test, y_test, predict_function, title="Decision Boundaries"):
    """
    Visualizes decision boundaries for a classifier.

    Parameters:
    - X_train: list of training feature vectors (2D)
    - y_train: list of training labels
    - X_test: list of test feature vectors
    - y_test: list of true test labels
    - predict_function: a function that takes a point [x, y] and returns a predicted class
    - title: plot title
    """
    # Check if the data is 2D
    if len(X_train[0]) != 2:
        print("Error: Can only visualize 2D data. Your data has", len(X_train[0]), "dimensions.")
        return

    plt.figure(figsize=(10, 8))

    # Get unique classes and prepare colors
    unique_classes = sorted(list(set(y_train)))
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
    cmap = ListedColormap(colors[:len(unique_classes)])

    # Determine the plot boundaries
    x_min, x_max = min(p[0] for p in X_train + X_test) - 1, max(p[0] for p in X_train + X_test) + 1
    y_min, y_max = min(p[1] for p in X_train + X_test) - 1, max(p[1] for p in X_train + X_test) + 1

    # Create a mesh grid
    h = 0.2  # step size in the mesh
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict class for each point in the mesh
    Z = []
    for i in range(len(xx.ravel())):
        x_val, y_val = xx.ravel()[i], yy.ravel()[i]
        Z.append(predict_function([x_val, y_val]))

    Z = np.array(Z).reshape(xx.shape)

    # Plot the decision boundary
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)

    # Plot training points
    for i, class_label in enumerate(unique_classes):
        indices = [j for j, label in enumerate(y_train) if label == class_label]
        class_points = [X_train[j] for j in indices]

        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'Class {class_label} (train)',
                    marker='o', alpha=0.7, edgecolor='k')

    # Plot test points
    for i, class_label in enumerate(unique_classes):
        indices = [j for j, label in enumerate(y_test) if label == class_label]
        class_points = [X_test[j] for j in indices]

        if not class_points:
            continue

        x_coords = [point[0] for point in class_points]
        y_coords = [point[1] for point in class_points]

        color = colors[i % len(colors)]
        plt.scatter(x_coords, y_coords, color=color, label=f'Class {class_label} (test)',
                    marker='s', alpha=1.0, s=80, edgecolor='k')

    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png")
    plt.show()


# Example usage with dummy prediction functions
if __name__ == "__main__":
    import numpy as np  # Only for the decision boundary example

    try:
        # Load data
        print("Loading data for visualization...")

        with open("data/classification_data.pkl", 'rb') as f:
            classification_data = pickle.load(f)
            X_train, y_train, X_test, y_test = classification_data

        with open("data/clustering_data.pkl", 'rb') as f:
            clustering_data = pickle.load(f)
            X_cluster, true_labels = clustering_data

        # Generate some mock predictions for demonstration
        # In real use, these would come from your ML algorithms

        # Mock k-NN predictions
        # Here we're simulating 80% accuracy for demonstration
        y_pred = y_test.copy()
        import random

        random.seed(42)
        for i in range(len(y_pred) // 5):  # Introduce ~20% errors
            idx = random.randint(0, len(y_pred) - 1)
            y_pred[idx] = 1 - y_pred[idx]  # Flip the binary label

        # Mock k-means predictions
        # Here we're just randomly permuting the cluster labels for demonstration
        predicted_clusters = true_labels.copy()
        random.shuffle(predicted_clusters)

        # Mock centers for k-means
        unique_clusters = list(set(true_labels))
        mock_centers = []
        for cluster_idx in unique_clusters:
            points = [X_cluster[i] for i in range(len(X_cluster)) if true_labels[i] == cluster_idx]
            center_x = sum(p[0] for p in points) / len(points)
            center_y = sum(p[1] for p in points) / len(points)
            mock_centers.append([center_x, center_y])

        # Visualize classification results
        print("\nVisualizing classification results...")
        visualize_classification_results(X_train, y_train, X_test, y_test, y_pred,
                                         "K-NN Classification Results")

        # Visualize clustering comparison
        print("\nVisualizing clustering comparison...")
        visualize_clustering_comparison(X_cluster, true_labels, predicted_clusters,
                                        mock_centers, "K-means Clustering Results")


        # Mock prediction function for decision boundaries
        def mock_predict_function(point):
            # Simple linear boundary for demonstration
            return 1 if point[0] + point[1] > 0 else 0


        # Visualize decision boundaries
        print("\nVisualizing decision boundaries...")
        try:
            visualize_decision_boundaries(X_train, y_train, X_test, y_test,
                                          mock_predict_function, "K-NN Decision Boundaries")
        except NameError:
            print("Note: The decision boundary visualization requires numpy for meshgrid.")
            print("If you want to use this function, please ensure numpy is available.")

    except FileNotFoundError:
        print("Data files not found. Run the data generation script first to create the data files.")

    except Exception as e:
        print(f"An error occurred: {e}")
