from math import fsum, sqrt
from pathlib import Path
from random import Random

import numpy as np
from matplotlib.figure import Figure
from scipy.stats import chi2, norm


MU = 9              # Математическое ожидание
SIGMA = 2           # Стандартное отклонение
N_SUMMANDS = 13     # Число слагаемых для одного значения
SAMPLE_SIZE = 1800  # Объём выборки
BINS = 23           # Число интервалов гистограммы
SEED = 42           # Начальное значение генератора


def generate_sample(size):
    rng = Random(SEED)
    sample = []
    for _ in range(size):
        uniform_sum = sum(rng.random() for _ in range(N_SUMMANDS))
        standard_value = sqrt(12 / N_SUMMANDS) * (uniform_sum - N_SUMMANDS / 2)
        sample.append(MU + SIGMA * standard_value)
    return sample


def estimate_statistics(sample):
    size = len(sample)
    mean = fsum(sample) / size
    deviations = [value - mean for value in sample]
    variance = fsum(d**2 for d in deviations) / (size - 1)
    m3 = fsum(d**3 for d in deviations) / size
    m4 = fsum(d**4 for d in deviations) / size

    corrected_m3 = size**2 * m3 / ((size - 1) * (size - 2))
    denominator = (size - 1) * (size**2 - 3 * size + 3)
    corrected_m4 = (size**3 * m4 - size**2 * variance**2 / (size - 1)) / denominator
    skewness = corrected_m3 / variance**1.5
    excess = corrected_m4 / variance**2 - 3
    return mean, variance, skewness, excess


sample = generate_sample(SAMPLE_SIZE)
estimates = estimate_statistics(sample)
size = len(sample)

distribution = norm(loc=MU, scale=SIGMA)
counts, edges = np.histogram(sample, bins=BINS)
widths = np.diff(edges)
heights = counts / (size * widths)

figure = Figure(figsize=(9, 5), layout="constrained")
axes = figure.subplots()
axes.bar(edges[:-1], heights, width=widths, align="edge",
         color="#6fa8cc", edgecolor="white", label="Выборка")
x = np.linspace(edges[0], edges[-1], 401)
axes.plot(x, distribution.pdf(x), color="#a23b28", linewidth=2,
          label="Теоретическая нормальная плотность")
axes.set(title="Метод суммирования. Вариант 19", xlabel="x", ylabel="Плотность")
axes.legend()
output = Path("lab5_variant19_histogram.png")
figure.savefig(output, dpi=160)

cdf = [0.0, *distribution.cdf(edges[1:-1]), 1.0]
expected = size * np.diff(cdf)
if min(expected) < 5:
    raise ValueError("Для критерия Пирсона нужно объединить интервалы с малой ожидаемой частотой.")

statistic = fsum((counts - expected)**2 / expected)
degrees_of_freedom = BINS - 1  
p_value = chi2.sf(statistic, degrees_of_freedom)

print(f"Вариант 19: μ = {MU}, σ = {SIGMA}, n = {N_SUMMANDS}, N = {SAMPLE_SIZE}, K = {BINS}")
print(f"Начальное значение генератора: {SEED}")
print(f"\n{'Характеристика':<24}{'Точное':>12}{'Оценка':>12}")
names = ("Математическое ожидание", "Дисперсия", "Асимметрия", "Эксцесс")
theoretical = (MU, SIGMA**2, 0, 0)
for name, exact, estimate in zip(names, theoretical, estimates):
    print(f"{name:<24}{exact:>12.4f}{estimate:>12.4f}")

print(f"\nКритерий Пирсона: χ² = {statistic:.4f}, групп = {BINS}, степеней свободы = {degrees_of_freedom}")
print(f"p-значение: {p_value:.6f}")
if p_value < 0.05:
    print("При α = 0.05 гипотеза о нормальном законе отвергается.")
else:
    print("При α = 0.05 оснований отвергнуть гипотезу о нормальном законе нет.")
print(f"\nГистограмма сохранена: {output.resolve()}")
