import cv2
import numpy as np
import matplotlib.pyplot as plt

# Функція для додавання шуму "сіль та перець" (Пункт 6)
def salt_and_pepper_noise(image, prob):
    output = np.copy(image)
    white = np.random.rand(image.shape[0], image.shape[1]) < prob
    black = np.random.rand(image.shape[0], image.shape[1]) < prob
    output[white] = 255
    output[black] = 0
    return output

# Пункт 4: Завантаження сірого зображення
gray_image = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)

# Пункт 5: Вирівнювання гістограми
equalized_image = cv2.equalizeHist(gray_image)

# Пункт 5: Гамма-корекція
gamma1 = 0.5
gamma2 = 2.0
gamma_corrected1 = np.array(255 * (gray_image / 255) ** gamma1, dtype='uint8')
gamma_corrected2 = np.array(255 * (gray_image / 255) ** gamma2, dtype='uint8')

# Пункт 6: Додавання шуму "сіль та перець"
noisy_image = salt_and_pepper_noise(gray_image, 0.05)

# Пункт 7: Вирівнювання шумного зображення
equalized_noisy_image = cv2.equalizeHist(noisy_image)

# Пункт 7: Застосування розмиття та медіанного фільтра
blurred_image = cv2.blur(noisy_image, (3, 3))
median_filtered = cv2.medianBlur(noisy_image, 3)

# Пункт 8: Виявлення країв за допомогою оператора Собеля
sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
sobel_combined = cv2.magnitude(sobelx, sobely)

# Пункт 9: Виявлення країв за допомогою оператора Кенні
edges = cv2.Canny(gray_image, 100, 200)

# Пункт 1: Завантаження кольорового зображення
color_image = cv2.imread('img.png')

# Пункт 2: Перетворення до RGB та YUV
img_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
img_yuv = cv2.cvtColor(color_image, cv2.COLOR_BGR2YUV)

# Пункт 2: Розділення каналів
Y, U, V = cv2.split(img_yuv)
R, G, B = cv2.split(img_rgb)

# Побудова графіків (Пункт 3 та 12)
fig, axes = plt.subplots(16, 1, figsize=(8, 32))
axes = axes.ravel()

# Заголовки для кожного підграфіку
titles = ['Original RGB', 'Equalized Image', 'Gamma Corrected 0.5', 'Gamma Corrected 2.0',
          'Red Channel', 'Green Channel', 'Blue Channel', 'Sobel Edges',
          'Y (Luminance)', 'U (Chrominance)', 'V (Chrominance)', 'Noisy Image',
          'Equalized Noisy Image', 'Blurred Image (3x3)', 'Median Filtered Image', 'Canny Edges']

# Зображення для кожного підграфіку
images = [img_rgb, equalized_image, gamma_corrected1, gamma_corrected2,
          R, G, B, sobel_combined,
          Y, U, V, noisy_image,
          equalized_noisy_image, blurred_image, median_filtered, edges]

# Проходження по осях та зображеннях для побудови графіків
for i in range(len(images)):
    cmap = 'gray' if len(images[i].shape) == 2 else None
    axes[i].imshow(images[i], cmap=cmap)
    axes[i].set_title(titles[i], fontsize=14)
    axes[i].axis('off')

# Налаштування макету
plt.tight_layout()
plt.show()
