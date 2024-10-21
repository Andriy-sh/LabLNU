import numpy as np


def dft(data, inv):
    N = len(data)
    WN = 2 * np.pi / N
    if inv == 1:
        WN = -WN

    X_real = np.zeros(N)
    X_imag = np.zeros(N)

    for k in range(N):
        wk = k * WN
        for n in range(N):
            c = np.cos(n * wk)
            s = np.sin(n * wk)
            X_real[k] += data[n].real * c + data[n].imag * s
            X_imag[k] -= data[n].real * s - data[n].imag * c

        if inv == 1:
            X_real[k] /= N
            X_imag[k] /= N

    result = [complex(X_real[k], X_imag[k]) for k in range(N)]
    return result


def main():
    data_input = input("Ввеcти послідовність : ")
    data = list(map(float, data_input.split()))
    data = [complex(x, 0) for x in data]

    direct_result = dft(data, inv=0)

    inverse_result = dft(direct_result, inv=1)

    print("Результат прямого ДПФ:")
    for r in direct_result:
        print(f"{r.real:.3f} + {r.imag:.3f}j")

    print("\nРезультат оберненого ДПФ:")
    for r in inverse_result:
        print(f"{r.real:.3f} + {r.imag:.3f}j")


if __name__ == "__main__":
    main()
#4 2 1 4 6 3 5 2