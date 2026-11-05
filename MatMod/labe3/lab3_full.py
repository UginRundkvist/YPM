"""Лабораторная № 3, вариант 19: моделирование методом Неймана.

Зависимости: numpy, matplotlib.
Запуск: python3 lab3.py
Результаты записываются в папку results рядом с программой.
"""

from pathlib import Path
import argparse
import csv
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "lab3_mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

A, B = 0.0, 2.0
C = 5 / (8 * np.sqrt(2))
M0 = 5 / 4  # Верхняя грань плотности на (0, 2).
MEAN = 10 / 7
VARIANCE = 80 / 441
SIZES = (10, 100, 2500)
BINS = 20


def density(x):
    """Плотность; значения в концах интервала приняты равными нулю."""
    x = np.asarray(x, dtype=float)
    return C * np.maximum(x, 0) ** 1.5 * ((x > A) & (x < B))


def cdf(x):
    """Точная функция распределения для проверки вероятностей интервалов."""
    return (np.clip(np.asarray(x, dtype=float), A, B) / 2) ** 2.5


def neyman(size, rng):
    """Принимаем x ~ U(0,2), если y ~ U(0,5/4) лежит под g(x)."""
    sample = []
    attempts = 0
    while len(sample) < size:
        x = rng.uniform(A, B)
        y = rng.uniform(0, M0)
        attempts += 1
        if y < density(x):
            sample.append(x)
    return np.array(sample), attempts


def write_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=19, help="Начальное состояние генератора")
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    # Независимые воспроизводимые выборки для трех объемов.
    seeds = np.random.SeedSequence(args.seed).spawn(len(SIZES))
    edges = np.linspace(A, B, BINS + 1)
    centers = (edges[:-1] + edges[1:]) / 2
    widths = np.diff(edges)
    grid = np.linspace(A, B, 600)
    # На графике показываем односторонние пределы плотности в концах.
    curve = C * grid ** 1.5
    fig, axes = plt.subplots(3, 2, figsize=(12, 12), constrained_layout=True)
    summary = []
    text = [
        "Лабораторная работа № 3. Вариант 19. Метод Неймана.",
        "g(x) = C*x^(3/2), 0 < x < 2; вне интервала g(x) = 0.",
        f"C = 5/(8*sqrt(2)) = {C:.10f}",
        f"M(X) = 10/7 = {MEAN:.10f}",
        f"E(X^2) = 20/9 = {20/9:.10f}",
        f"D(X) = 80/441 = {VARIANCE:.10f}",
        "Огибающий прямоугольник: (0,2) x (0,5/4).",
        "Теоретическая вероятность принятия: 1/(2*5/4) = 0.4.",
        f"Seed = {args.seed}. Гистограмма: {BINS} интервалов, ширина 0.1.",
        "D_hat = sum((x - mean)^2)/N; S^2 = sum((x - mean)^2)/(N-1).",
        "Относительная частота = count/N; плотность = count/(N*width).",
        "",
    ]
    for row, (size, seed) in enumerate(zip(SIZES, seeds)):
        sample, attempts = neyman(size, np.random.default_rng(seed))
        counts, _ = np.histogram(sample, bins=edges)
        frequencies = counts / size
        empirical = frequencies / widths
        theoretical = density(centers)
        errors = np.abs(theoretical - empirical)
        mean = float(np.mean(sample))
        variance = float(np.var(sample, ddof=0))
        corrected = float(np.var(sample, ddof=1))
        summary.append((size, mean, variance, corrected, abs(mean - MEAN),
                        abs(variance - VARIANCE), attempts, size / attempts))
        write_csv(args.out / f"sample_{size}.csv", ["i", "x"], enumerate(sample, 1))
        write_csv(args.out / f"histogram_{size}.csv",
                  ["left", "right", "center", "count", "relative_frequency",
                   "density_estimate", "theoretical_density", "absolute_error",
                   "exact_bin_probability"],
                  zip(edges[:-1], edges[1:], centers, counts, frequencies, empirical,
                      theoretical, errors, np.diff(cdf(edges))))
        ax, error_ax = axes[row]
        ax.bar(centers, empirical, width=widths, color="#80b5db", edgecolor="white",
               label="Выборочная плотность")
        ax.plot(grid, curve, color="#b32930", linewidth=2, label="Точная плотность g(x)")
        ax.set(title=f"Плотность и гистограмма, N = {size}", xlabel="x", ylabel="Плотность")
        ax.legend(fontsize=9)
        error_ax.plot(centers, errors, "o-", color="#6551a3", markersize=4)
        error_ax.set(title=f"|g(xᵢ) − ρ̂ᵢ|, N = {size}", xlabel="Центр интервала xᵢ",
                     ylabel="Абсолютное отклонение")
        for axis in (ax, error_ax):
            axis.set_xlim(A, B)
            axis.set_ylim(bottom=0)
            axis.grid(alpha=0.25)
            axis.set_axisbelow(True)
        text.extend([
            f"N = {size}",
            f"  Среднее: {mean:.10f}; абсолютная ошибка: {abs(mean-MEAN):.10f}",
            f"  Дисперсия (деление на N): {variance:.10f}; ошибка: {abs(variance-VARIANCE):.10f}",
            f"  Исправленная дисперсия (деление на N-1): {corrected:.10f}",
            f"  Попыток: {attempts}; доля принятых: {size/attempts:.6f}", "",
        ])
    fig.savefig(args.out / "graphs.png", dpi=160)
    plt.close(fig)
    write_csv(args.out / "summary.csv",
              ["N", "mean", "variance_N", "variance_N_minus_1", "mean_absolute_error",
               "variance_absolute_error", "attempts", "acceptance_rate"], summary)
    report = "\n".join(text)
    (args.out / "results.txt").write_text(report, encoding="utf-8")
    print(report)
    print(f"Результаты сохранены: {args.out.resolve()}")


if __name__ == "__main__":
    main()
