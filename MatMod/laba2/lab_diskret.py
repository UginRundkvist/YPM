import random
import matplotlib.pyplot as plt

random.seed(47)  # фиксирует выборку: числа совпадают с отчётом (строку можно убрать)

N = 110
q = 16

znacheniya = [-11, -1, 1]
veroyatnosti = [0.3, 0.6, 0.1]

# Моделируем выборку методом обратной функции.
# Отрезок [0;1] делим на части, длины которых равны вероятностям: границы —
# это накопленные суммы. Куда попало случайное число, то значение и выпало.
granicy = []
summa_p = 0.0
for i in range(len(veroyatnosti)):
    summa_p = summa_p + veroyatnosti[i]
    granicy.append(summa_p)
granicy[len(granicy) - 1] = 1.0

x = []
for i in range(N):
    r = random.random()
    k = 0
    while r >= granicy[k]:
        k += 1
    x.append(znacheniya[k])

print(f"Первые {q} смоделированных значений:")
for i in range(q):
    print(f"{i + 1}: {x[i]}")

# Точные характеристики считаются прямо по закону распределения:
# среднее — сумма произведений вероятности на значение,
# дисперсия — сумма произведений вероятности на квадрат значения минус квадрат среднего.
M = 0.0
for i in range(len(znacheniya)):
    M += veroyatnosti[i] * znacheniya[i]

D = 0.0
for i in range(len(znacheniya)):
    D += veroyatnosti[i] * znacheniya[i] * znacheniya[i]
D = D - M * M

# Те же характеристики, восстановленные по выборке. Среднее считаем полностью
# и только потом подставляем в формулу дисперсии, поэтому циклов два.
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

# График: частости по выборке рядом с заданными вероятностями.
chastosti = []
for i in range(len(znacheniya)):
    skolko = 0
    for j in range(N):
        if x[j] == znacheniya[i]:
            skolko += 1
    chastosti.append(skolko / N)

nomera = list(range(len(znacheniya)))
plt.bar([i - 0.19 for i in nomera], chastosti, width=0.38,
        color="#3d6e99", edgecolor="black", label="Частость по выборке")
plt.bar([i + 0.19 for i in nomera], veroyatnosti, width=0.38,
        color="#c0392b", edgecolor="black", label="Заданная вероятность")
plt.xticks(nomera, [str(v) for v in znacheniya])
plt.xlabel("Значения случайной величины")
plt.ylabel("Вероятность / частость")
plt.title("Сравнение эмпирических частостей и заданных вероятностей")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()