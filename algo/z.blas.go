package main

import (
	"fmt"
	m "math"
)

func dvasum(v []float64) float64 {
	var ret float64 = 0.
	for _, vi := range v {
		ret += m.Abs(vi)
	}
	return ret
}

func main() {
	fmt.Println("Naive BLAS TEST")
	var v []float64 = []float64{1, -1, 2, -2}
	fmt.Println(dvasum(v))
}
