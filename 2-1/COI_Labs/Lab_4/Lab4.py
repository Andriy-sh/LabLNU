import numpy as np


def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]


def ifft(x):
    N = len(x)
    x_conj = np.conjugate(x)
    result = fft(x_conj)
    return np.conjugate(result) / N


def main():
    data = list(map(int, input("Ввести послідовність: ").split()))

    while len(data) & (len(data) - 1) != 0:
        data.append(0)

    data = np.array(data, dtype=complex)

    fft_result = fft(data)
    print("Результат прямого ШПФ:")
    for r in fft_result:
        print(f"{r.real:.3f} + {r.imag:.3f}j")

    ifft_result = ifft(fft_result)
    print("\nРезультат оберненого ШПФ:")
    for r in ifft_result:
        print(f"{r.real:.3f} + {r.imag:.3f}j")


if __name__ == "__main__":
    main()
#5 7 3 3 0 0 15 32 13 7