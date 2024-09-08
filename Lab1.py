def discrete_convolution(x, y):
    n = len(x)
    m = len(y)
    result = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += x[i] * y[m - j - 1]
    return result

x = [4, 1, 1]
y = [7, 4, 5]
convolution_result = discrete_convolution(x, y)
print(f"Результат згортки: {convolution_result}")
x = [9, 8, 7, 4, 9, 5, 0]
y = [5, 3, 2, 4, 0, 1, 2]
convolution_result = discrete_convolution(x, y)
print(f"Результат згортки: {convolution_result}")
x = [7, 1, 9, 8, 7, 5]
y = [8, 7, 3, 4, 6, 0, 9, 2, 1, 6]
convolution_result = discrete_convolution(x, y)
print(f"Результат згортки: {convolution_result}")
