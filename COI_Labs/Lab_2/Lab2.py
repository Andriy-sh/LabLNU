import numpy as np

x1 = np.array([9, 8, 7, 4, 9, 5, 0])
x2 = np.array([7, 1, 9, 8, 7, 5])
y1 = np.array([5, 3, 2, 4, 0, 1, 2])
y2 = np.array([8, 7, 3, 4, 6, 0, 9, 2, 1, 6])

def scale_signal(signal, num):
    return signal * num

def reverse_signal(signal):
    return signal[::-1]

def shift_signal(signal, num):
    return np.roll(signal, num)

def expand_signal(signal, num):
    expanded = np.zeros(len(signal) * num)
    expanded[::num] = signal
    return expanded

def add_signals(signal1, signal2):
    return signal1 + signal2

def multiply_signals(signal1, signal2):
    return signal1 * signal2

scaled_x1 = scale_signal(x1, 10)
print(f"Масштабований сигнал x1: {scaled_x1}")
reversed_x1 = reverse_signal(x1)
print(f"Реверс сигналу x1: {reversed_x1}")
shifted_x1 = shift_signal(x1, 3)
print(f"Зсув сигналу x1 на 3 позиції: {shifted_x1}")
expanded_x1 = expand_signal(x1, 2)
print(f"Розширений сигнал x1: {expanded_x1}")
added_signals = add_signals(x1, y1)
print(f"Додавання сигналів x1 та y1: {added_signals}")
multiplied_signals = multiply_signals(x1, y1)
print(f"Множення сигналів x1 та y1: {multiplied_signals}")

