def discrete_convolution(x, y):
    n = len(x)
    m = len(y)
    result = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += x[i] * y[m - j - 1]
    return result

x = [3, 2, 1]
y = [1, 2, 3]
convolution_result = discrete_convolution(x, y)
print(f"Результат згортки: {convolution_result}")
x = [3, 2, 1]
y =  [1, 2, 3]
convolution_result = discrete_convolution(x, y)
print(f"Результат згортки: {convolution_result}")
x = [7, 1, 9, 8, 7, 5]
y = [8, 7, 3, 4, 6, 0, 9, 2, 1, 6]
convolution_result = discrete_convolution(x, y)
print(f"Результат згортки: {convolution_result}")

# while True:
#     x=list(map(int,input("x = ").split()))
#     if x is None:
#         break
#     y = list(map(int, input("y = ").split()))
#     if y is None:
#         break
#     result = discrete_convolution(x,y)
#     print(result)