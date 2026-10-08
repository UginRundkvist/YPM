import random

N = 110
q = 16

znacheniya = [-11, -1, 1]
veroyatnosti = [0.3, 0.6, 0.1]

# Моделируем выборку методом обратной функции.
# Отрезок [0;1] делим на части, длины которых равны вероятностям: границы это накопленные суммы. Куда попало случайное число, то значение и выпало.
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

print(f"1-2) Первые {q} значений выборки:")
for i in range(q):
    print(f"x[{i + 1}] = {x[i]}")

# Точные характеристики считаются прямо по закону распределения:
# среднее - сумма произведений вероятности на значение, дисперсия - сумма произведений вероятности на квадрат значения минус квадрат среднего.
M_tochnoe = 0.0
for i in range(len(znacheniya)):
    M_tochnoe += veroyatnosti[i] * znacheniya[i]

D_tochnoe = 0.0
for i in range(len(znacheniya)):
    D_tochnoe += veroyatnosti[i] * znacheniya[i] * znacheniya[i]
D_tochnoe = D_tochnoe - M_tochnoe * M_tochnoe

print("\n3) Точные значения:")
print(f"   M = {M_tochnoe:.4f}")
print(f"   D = {D_tochnoe:.4f}")

# Теперь те же характеристики, но восстановленные по выборке.
# Среднее — сумма значений делить на их количество.
# Сначала считаем среднее целиком и только потом подставляем его в дисперсию,
# поэтому циклов два, а не один.
summa = 0.0
for i in range(N):
    summa = summa + x[i]
m = summa / N

# Оценка дисперсии: сумма квадратов делить на (N - 1),
# минус N делить на (N - 1) и умножить на квадрат среднего.
summa_kvadratov = 0.0
for i in range(N):
    summa_kvadratov += x[i] * x[i]
g = summa_kvadratov / (N - 1) - N / (N - 1) * m * m

print("\n4) Оценки по выборке:")
print(f"   m = {m:.4f}   (точное {M_tochnoe:.4f}, отклонение {abs(m - M_tochnoe):.4f})")
print(f"   g = {g:.4f}   (точное {D_tochnoe:.4f}, отклонение {abs(g - D_tochnoe):.4f})")

# Частости должны получиться близкими к заданным вероятностям.
print("\n   Частоты появления значений:")
for i in range(len(znacheniya)):
    skolko = 0
    for j in range(N):
        if x[j] == znacheniya[i]:
            skolko += 1
    print(f"   {znacheniya[i]:4d}: выпало {skolko:3d} раз, частость {skolko / N:.4f} "
          f"(вероятность {veroyatnosti[i]})")

print("\n   Вывод: оценки близки к точным значениям, частости близки к заданным")
print("   вероятностям — моделирование методом обратной функции выполнено верно.")
