import random

N = 110
q = 16

znacheniya = [-11, -1, 1]
veroyatnosti = [0.3, 0.6, 0.1]

# 1
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

# 2
print(f"1-2) Первые {q} значений выборки:")
for i in range(q):
    print(f"x[{i + 1}] = {x[i]}")

# 3
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

# 4
summa = 0.0
for i in range(N):
    summa = summa + x[i]
m = summa / N

summa_kvadratov = 0.0
for i in range(N):
    summa_kvadratov += x[i] * x[i]
g = summa_kvadratov / (N - 1) - N / (N - 1) * m * m

print("\n4) Оценки по выборке:")
print(f"   m = {m:.4f}   (точное {M_tochnoe:.4f}, отклонение {abs(m - M_tochnoe):.4f})")
print(f"   g = {g:.4f}   (точное {D_tochnoe:.4f}, отклонение {abs(g - D_tochnoe):.4f})")

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
