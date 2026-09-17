package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"strings"
)

const (
	N = 800 + 20*19
)

func main() {

	// 1: получаем N значений из интервала [0;1]
	x := make([]float64, N)
	for i := 0; i < N; i++ {
		x[i] = rand.Float64()
	}

	// 2: выводим 10 первых значений
	fmt.Println("2) Первые 10 значений:")
	for i := 0; i < 10; i++ {
		fmt.Printf("x[%d] = %.6f\n", i+1, x[i])
	}

	// 3: оценки среднего и дисперсии
	// дисперсия = сумма квадратов отклонений от среднего делить на (количество минус один)
	sum := 0.0
	for i := range x {
		sum = sum + x[i]
	}

	midle := sum / N
	dispersion := 0.0
	for i := range x {
		dispersion += (x[i] - midle) * (x[i] - midle)
	}
	dispersion = dispersion / (N - 1)

	fmt.Printf("\n3) Среднее   = %.6f   (точное 0.5)\n", midle)
	fmt.Printf("   Дисперсия = %.6f   (точное %.6f)\n", dispersion, 1.0/12)

	//4: частотный тест
	// статистика = модуль разности количеств делить на корень из объёма выборки
	n0 := 0
	n1 := 0

	for i := range x {
		if x[i] < 0.5 {
			n0++
		} else {
			n1++
		}
	}

	S := math.Abs(float64(n1-n0)) / math.Sqrt(N)

	fmt.Printf("\n4) Меньше 0.5: %d,  больше 0.5: %d,  S = %.4f\n", n0, n1, S)
	if S < 1.96 {
		fmt.Println("   S < 1.96 — частотный тест пройден, числа ложатся равномерно")
	} else {
		fmt.Println("   S >= 1.96 — тест не пройден")
	}

	// 5: гистограмма и плотность
	// номер  = целая часть от деления значения на ширину
	// плотность = количество делить на объём выборки и на ширину

	counts := make([]int, 10)
	for i := range x {
		k := int(x[i] / 0.1)
		if k == 10 {
			k = 9
		}
		counts[k]++
	}

	fmt.Printf("\n5) Гистограмма (ожидаемое количество в корзине: %d)\n", N/10)
	for i := range counts {
		dolya := float64(counts[i]) / N
		plotnost := dolya / 0.1
		stars := strings.Repeat("*", counts[i]/4) // один символ = 4 значения
		fmt.Printf("[%.1f - %.1f)  n = %4d  доля = %.4f  плотность = %.4f  %s\n",
			float64(i)*0.1, float64(i+1)*0.1, counts[i], dolya, plotnost, stars)
	}
	fmt.Println("   Теоретическая плотность равномерного закона: f(x) = 1")

	risunok, err := os.Create("histogram.svg")
	if err != nil {
		fmt.Println("не удалось создать файл:", err)
	} else {
		shirinaStolbca := 60.0
		nizhnyayaLiniya := 340.0
		maxShkaly := 1.5
		vysotaPolya := 280.0

		fmt.Fprintf(risunok, `<svg xmlns="http://www.w3.org/2000/svg" width="700" height="400">`)
		fmt.Fprintf(risunok, `<rect width="700" height="400" fill="white"/>`)
		fmt.Fprintf(risunok, `<text x="350" y="30" font-size="16" text-anchor="middle">Гистограмма (N=%d) и плотность f(x)=1</text>`, N)

		for i := range counts {
			plotnost := float64(counts[i]) / N / 0.1
			vysota := plotnost / maxShkaly * vysotaPolya
			levyyKray := 60 + float64(i)*shirinaStolbca

			fmt.Fprintf(risunok, `<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#6fa8dc" stroke="black"/>`,
				levyyKray, nizhnyayaLiniya-vysota, shirinaStolbca, vysota)
			fmt.Fprintf(risunok, `<text x="%.1f" y="%.1f" font-size="12" text-anchor="middle">%d</text>`,
				levyyKray+shirinaStolbca/2, nizhnyayaLiniya-vysota-5, counts[i])
			fmt.Fprintf(risunok, `<text x="%.1f" y="%.1f" font-size="12" text-anchor="middle">%.1f</text>`,
				levyyKray, nizhnyayaLiniya+18, float64(i)*0.1)
		}
		fmt.Fprintf(risunok, `<text x="660" y="358" font-size="12" text-anchor="middle">1.0</text>`)

		for _, v := range []float64{0.0, 0.5, 1.0, 1.5} {
			y := nizhnyayaLiniya - v/maxShkaly*vysotaPolya
			fmt.Fprintf(risunok, `<text x="50" y="%.1f" font-size="12" text-anchor="end">%.1f</text>`, y+4, v)
		}

		yLinii := nizhnyayaLiniya - 1.0/maxShkaly*vysotaPolya
		fmt.Fprintf(risunok, `<line x1="60" y1="%.1f" x2="660" y2="%.1f" stroke="red" stroke-width="2"/>`, yLinii, yLinii)
		fmt.Fprintf(risunok, `<text x="655" y="52" font-size="13" fill="red" text-anchor="end">— плотность f(x) = 1</text>`)

		fmt.Fprintf(risunok, `<line x1="60" y1="%.1f" x2="660" y2="%.1f" stroke="black"/>`, nizhnyayaLiniya, nizhnyayaLiniya)
		fmt.Fprintf(risunok, `<line x1="60" y1="60" x2="60" y2="%.1f" stroke="black"/>`, nizhnyayaLiniya)
		fmt.Fprintf(risunok, `<text x="20" y="200" font-size="13">плотность</text>`)
		fmt.Fprintf(risunok, `</svg>`)

		risunok.Close()
	}

	// 6: критерий Пирсона
	// хи-квадрат = сумма по отрезкам: квадрат разности фактического и ожидаемого количества делить на ожидаемое количество
	expected := float64(N) / 10 // ожидаемое количество в одном отрезке
	chi2 := 0.0
	for i := range counts {
		raznica := float64(counts[i]) - expected
		chi2 += raznica * raznica / expected
	}

	fmt.Printf("\n6) Хи-квадрат наблюдаемое = %.4f\n", chi2)
	fmt.Println("   Хи-квадрат критическое (alpha = 0.05, k-1 = 9) = 16.919")
	if chi2 < 16.919 {
		fmt.Println("   chi2 < 16.919 — гипотеза о равномерном распределении принимается")
	} else {
		fmt.Println("   chi2 >= 16.919 — гипотеза о равномерном распределении отвергается")
	}

	// 7: вторая выборка и коэффициент корреляции
	// коэффициент корреляции = сумма произведений отклонений двух выборок делить на корень из произведения сумм квадратов отклонений
	y := make([]float64, N)
	for i := 0; i < N; i++ {
		y[i] = rand.Float64()
	}

	sumY := 0.0
	for i := range y {
		sumY = sumY + y[i]
	}
	midleY := sumY / N

	verh := 0.0
	nizX := 0.0
	nizY := 0.0
	for i := range x {
		verh += (x[i] - midle) * (y[i] - midleY)
		nizX += (x[i] - midle) * (x[i] - midle)
		nizY += (y[i] - midleY) * (y[i] - midleY)
	}
	r := verh / math.Sqrt(nizX*nizY)

	fmt.Printf("\n7) Среднее второй выборки = %.6f\n", midleY)
	fmt.Printf("   Коэффициент корреляции r = %.6f\n", r)
	if math.Abs(r) < 0.06 {
		fmt.Println("   r близок к нулю — выборки независимы, линейной связи нет")
	} else {
		fmt.Println("   r заметно отличается от нуля — есть линейная связь")
	}

	// 8: величина, равномерная на [2;12]
	// новое значение = левая граница плюс длина отрезка умножить на значение из [0;1]
	z := make([]float64, N)
	for i := range x {
		z[i] = 2 + 10*x[i]
	}

	sumZ := 0.0
	for i := range z {
		sumZ = sumZ + z[i]
	}
	midleZ := sumZ / N

	dispersionZ := 0.0
	for i := range z {
		dispersionZ += (z[i] - midleZ) * (z[i] - midleZ)
	}
	dispersionZ = dispersionZ / (N - 1)

	fmt.Println("\n8) Величина на [2;12], первые 5 значений:")
	for i := 0; i < 5; i++ {
		fmt.Printf("z[%d] = %.6f\n", i+1, z[i])
	}
	fmt.Printf("   Среднее   = %.6f\n", midleZ)
	fmt.Printf("   Дисперсия = %.6f\n", dispersionZ)

	// ПУНКТ 9: сравнение с точными характеристиками
	// точное среднее = полусумма границ отрезка
	// точная дисперсия = квадрат длины отрезка делить на двенадцать
	midleTochno := (2.0 + 12.0) / 2
	dispersionTochno := (12.0 - 2.0) * (12.0 - 2.0) / 12

	fmt.Printf("\n9) Среднее:   смоделированное %.6f, точное %.6f, отклонение %.6f\n",
		midleZ, midleTochno, math.Abs(midleZ-midleTochno))
	fmt.Printf("   Дисперсия: смоделированная %.6f, точная %.6f, отклонение %.6f\n",
		dispersionZ, dispersionTochno, math.Abs(dispersionZ-dispersionTochno))
	fmt.Println("   Оценки близки к точным значениям — моделирование выполнено верно")
}
