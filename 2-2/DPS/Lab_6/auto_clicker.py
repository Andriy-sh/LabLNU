import pyautogui
import time
import random

# Координати точки на екрані (замініть на потрібні значення)
x, y = 1800, 920

print("Запускаю безкінечні кліки. Натисніть Ctrl+C, щоб зупинити.")

try:
    while True:
        # Виконуємо клік
        pyautogui.click(x, y)
        print(f"Клік на координатах ({x}, {y}) виконано.")

        # Генеруємо випадковий час у діапазоні від 3 до 7 секунд
        interval = random.uniform(3, 7)
        print(f"Чекаю {interval:.2f} секунд...")
        time.sleep(interval)
except KeyboardInterrupt:
    print("Скрипт зупинено.")