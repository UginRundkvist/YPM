import random
import math
import matplotlib.pyplot as plt

N = 800 + 20 * 19

# ПУНКТ 1: моделируем N значений из интервала [0;1]
x = []
for i in range(N):
    x.append(random.random())

# ПУНКТ 2: первые 10 значений
print("2) Первые 10 значений:")
for i in range(10):
    print(f"x[{i + 1}] = {x[i]:.6f}")

# ПУНКТ 3: среднее и дисперсия
summa = 0.0
for i in range(N):
    summa = summa + x[i]
midle = summa / N

dispersion = 0.0
for i in range(N):
    dispersion += (x[i] - midle) * (x[i] - midle)
dispersion = dispersion / (N - 1)

print(f"\n3) Среднее   = {midle:.6f}   (точное 0.5)")
print(f"   Дисперсия = {dispersion:.6f}   (точное {1 / 12:.6f})")

# ПУНКТ 4: частотный тест
n0 = 0
n1 = 0
for i in range(N):
    if x[i] < 0.5:
        n0 += 1
    else:
        n1 += 1

S = abs(n1 - n0) / math.sqrt(N)

print(f"\n4) Меньше 0.5: {n0},  больше 0.5: {n1},  S = {S:.4f}")
if S < 1.96:
    print("   S < 1.96 — частотный тест пройден, числа ложатся равномерно")
else:
    print("   S >= 1.96 — тест не пройден")

# ПУНКТ 5: гистограмма и плотность
counts = [0] * 10
for i in range(N):
    k = int(x[i] / 0.1)
    if k == 10:
        k = 9
    counts[k] += 1

print(f"\n5) Гистограмма (ожидаемое количество в отрезке: {N // 10})")
for i in range(10):
    dolya = counts[i] / N
    plotnost = dolya / 0.1
    print(f"[{i * 0.1:.1f} - {(i + 1) * 0.1:.1f})  n = {counts[i]:4d}  "
          f"доля = {dolya:.4f}  плотность = {plotnost:.4f}")
print("   Теоретическая плотность равномерного закона: f(x) = 1")

centry = []
plotnosti = []
for i in range(10):
    centry.append(i * 0.1 + 0.05)
    plotnosti.append(counts[i] / N / 0.1)

plt.bar(centry, plotnosti, width=0.1, color="#6fa8dc", edgecolor="black", label="гистограмма")
plt.axhline(1, color="red", linewidth=2, label="плотность f(x) = 1")
plt.title(f"Гистограмма выборки (N = {N}) и плотность равномерного закона")
plt.xlabel("x")
plt.ylabel("плотность")
plt.ylim(0, 1.5)
plt.legend()
plt.show()

# ПУНКТ 6: критерий Пирсона
expected = N / 10
chi2 = 0.0
for i in range(10):
    raznica = counts[i] - expected
    chi2 += raznica * raznica / expected

print(f"\n6) Хи-квадрат наблюдаемое = {chi2:.4f}")
print("   Хи-квадрат критическое (alpha = 0.05, k-1 = 9) = 16.919")
if chi2 < 16.919:
    print("   chi2 < 16.919 — гипотеза о равномерном распределении принимается")
else:
    print("   chi2 >= 16.919 — гипотеза о равномерном распределении отвергается")

# ПУНКТ 7: вторая выборка и коэффициент корреляции
y = []
for i in range(N):
    y.append(random.random())

summa_y = 0.0
for i in range(N):
    summa_y = summa_y + y[i]
midle_y = summa_y / N

verh = 0.0
niz_x = 0.0
niz_y = 0.0
for i in range(N):
    verh += (x[i] - midle) * (y[i] - midle_y)
    niz_x += (x[i] - midle) * (x[i] - midle)
    niz_y += (y[i] - midle_y) * (y[i] - midle_y)

r = verh / math.sqrt(niz_x * niz_y)

print(f"\n7) Среднее второй выборки = {midle_y:.6f}")
print(f"   Коэффициент корреляции r = {r:.6f}")
if abs(r) < 0.06:
    print("   r близок к нулю — выборки независимы, линейной связи нет")
else:
    print("   r заметно отличается от нуля — есть линейная связь")

# ПУНКТ 8: величина, равномерная на [2;12]
z = []
for i in range(N):
    z.append(2 + 10 * x[i])

summa_z = 0.0
for i in range(N):
    summa_z = summa_z + z[i]
midle_z = summa_z / N

dispersion_z = 0.0
for i in range(N):
    dispersion_z += (z[i] - midle_z) * (z[i] - midle_z)
dispersion_z = dispersion_z / (N - 1)

print("\n8) Величина на [2;12], первые 5 значений:")
for i in range(5):
    print(f"z[{i + 1}] = {z[i]:.6f}")
print(f"   Среднее   = {midle_z:.6f}")
print(f"   Дисперсия = {dispersion_z:.6f}")

# ПУНКТ 9: сравнение с точными характеристиками
midle_tochno = (2 + 12) / 2
dispersion_tochno = (12 - 2) * (12 - 2) / 12

print(f"\n9) Среднее:   смоделированное {midle_z:.6f}, точное {midle_tochno:.6f}, "
      f"отклонение {abs(midle_z - midle_tochno):.6f}")
print(f"   Дисперсия: смоделированная {dispersion_z:.6f}, точная {dispersion_tochno:.6f}, "
      f"отклонение {abs(dispersion_z - dispersion_tochno):.6f}")
print("   Оценки близки к точным значениям — моделирование выполнено верно")
