import random
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


C = 5 / (8 * np.sqrt(2))
M = 10 / 7
D = 80 / 441


def g(x):
    return C * x ** 1.5  


def neyman(n):
    sample = []
    while len(sample) < n:
        x = random.uniform(0, 2)
        y = random.uniform(0, 1.25)
        if y < g(x):
            sample.append(x)
    return np.array(sample)


random.seed(19)
folder = Path(__file__).resolve().parent / 'results_simple'
folder.mkdir(exist_ok=True)

text = f'C = {C:.6f}\nТочное среднее = {M:.6f}\nТочная дисперсия = {D:.6f}\n'
x = np.linspace(0, 2, 200)
fig, axes = plt.subplots(3, 2, figsize=(11, 10))

for i, n in enumerate([10, 100, 2500]):
    sample = neyman(n)
    mean = sum(sample) / n
    variance = sum((sample - mean) ** 2) / n

    text += f'\nN = {n}\nСреднее = {mean:.6f}\nДисперсия = {variance:.6f}\n'
    text += f'Ошибка среднего = {abs(mean - M):.6f}\n'
    text += f'Ошибка дисперсии = {abs(variance - D):.6f}\n'
    np.savetxt(folder / f'sample_{n}.txt', sample, fmt='%.10f')

    # 20 интервалов шириной 0.1
    counts, edges = np.histogram(sample, bins=20, range=(0, 2))
    centers = (edges[:-1] + edges[1:]) / 2
    density = counts / (n * 0.1)
    error = abs(g(centers) - density)

    axes[i, 0].bar(centers, density, width=0.1, edgecolor='white')
    axes[i, 0].plot(x, g(x), 'r', label='g(x)')
    axes[i, 0].set_title(f'Гистограмма, N = {n}')
    axes[i, 0].set_ylabel('Плотность')
    axes[i, 0].legend()

    axes[i, 1].plot(centers, error, 'o-')
    axes[i, 1].set_title(f'Отклонение от g(x), N = {n}')
    axes[i, 1].set_ylabel('Абсолютное отклонение')

    for ax in axes[i]:
        ax.set_xlabel('x')
        ax.set_xlim(0, 2)
        ax.set_ylim(bottom=0)
        ax.grid(alpha=0.3)

print(text)
(folder / 'results.txt').write_text(text, encoding='utf-8')
plt.tight_layout()
plt.savefig(folder / 'graphs.png', dpi=150)
plt.show()
