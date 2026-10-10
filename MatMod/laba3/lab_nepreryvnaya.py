import random
import math
import matplotlib.pyplot as plt

random.seed(11)  # фиксирует выборку: числа совпадают с отчётом (строку можно убрать)

N = 80
q = 12

a = -math.pi / 6  # левая граница интервала
b = math.pi / 3   # правая граница интервала


# Плотность распределения по варианту 19:
# корень из трёх делить на четыре, делить на квадрат косинуса.
def plotnost(t):
    return math.sqrt(3) / (4 * math.cos(t) * math.cos(t))


# Моделируем выборку методом обратной функции.
# Интеграл от плотности даёт функцию распределения F(x) = (корень из трёх / 4) * tg x + 1/4.
# Приравняв её к случайному числу r и выразив x, получаем арктангенс от (4r - 1) / корень из трёх.
x = []
for i in range(N):
    r = random.random()
    x.append(math.atan((4 * r - 1) / math.sqrt(3)))

print(f"Первые {q} смоделированных значений:")
for i in range(q):
    print(f"{i + 1}: {x[i]:.4f}")

# Точные характеристики — интегралы по интервалу: среднее от значения на плотность,
# дисперсия от квадрата значения на плотность минус квадрат среднего.
# Берём их численно, методом трапеций.
shagov = 100000
shag = (b - a) / shagov

M = 0.0
for i in range(shagov):
    t1 = a + i * shag
    t2 = t1 + shag
    M += (t1 * plotnost(t1) + t2 * plotnost(t2)) / 2 * shag

M_kvadrata = 0.0
for i in range(shagov):
    t1 = a + i * shag
    t2 = t1 + shag
    M_kvadrata += (t1 * t1 * plotnost(t1) + t2 * t2 * plotnost(t2)) / 2 * shag

D = M_kvadrata - M * M

# Те же характеристики по выборке: среднее считаем полностью и только потом
# подставляем в формулу дисперсии.
summa = 0.0
for i in range(N):
    summa = summa + x[i]
m = summa / N

summa_kvadratov = 0.0
for i in range(N):
    summa_kvadratov += x[i] * x[i]
g = summa_kvadratov / (N - 1) - N / (N - 1) * m * m

print("-" * 46)
print(f"Точное математическое ожидание (M): {M:.4f}")
print(f"Оценка математического ожидания (m): {m:.4f}")
print(f"Разница (ошибка): {abs(m - M):.4f}")
print("-" * 46)
print(f"Точная дисперсия (D): {D:.4f}")
print(f"Оценка дисперсии (g): {g:.4f}")
print(f"Разница (ошибка): {abs(g - D):.4f}")

# График: гистограмма выборки и теоретическая плотность.
setka = []
znacheniya_plotnosti = []
for i in range(401):
    t = a + (b - a) * i / 400
    setka.append(t)
    znacheniya_plotnosti.append(plotnost(t))

plt.hist(x, bins=8, range=(a, b), density=True,
         color="#3d6e99", edgecolor="black", label="Эмпирическая плотность")
plt.plot(setka, znacheniya_plotnosti, color="#c0392b", linewidth=2.5,
         label="Теоретическая плотность f(x)")
plt.xlabel("Значения x")
plt.ylabel("Плотность вероятности")
plt.title("Сравнение эмпирической и теоретической плотностей распределения")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()