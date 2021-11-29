package main

import (
	"fmt"
)

func bSort(v []int) {
	for i := 0; i < len(v); i++ {
		dirty := false
		for j := len(v) - 1; j > 0; j-- {
			if v[j] < v[j-1] {
				v[j], v[j-1] = v[j-1], v[j]
				dirty = true
			}
		}
		if !dirty {
			break
		}
	}
}

func selSort(v []int) {
	for i := 0; i < len(v); i++ {
		idxmin := i
		for j := i; j < len(v); j++ {
			if v[j] < v[idxmin] {
				idxmin = j
			}
		}
		v[i], v[idxmin] = v[idxmin], v[i]
	}
}

func naiveSort(v []int) {
	for i := 0; i < len(v); i++ {
		for j := i; j < len(v); j++ {
			if v[j] < v[i] {
				v[i], v[j] = v[j], v[i]
			}
		}
	}
}

func _qSort(v []int, curl int, curr int) {
	if curl < curr {
		i, j := curl, curr
		pivot := v[i]
		for i < j {
			for i < j && v[j] > pivot {
				j--
			}
			if i < j {
				v[i] = v[j]
				i++
			}
			for i < j && v[i] < pivot {
				i++
			}
			if i < j {
				v[j] = v[i]
				j--
			}
		}
		v[i] = pivot
		_qSort(v, curl, i-1)
		_qSort(v, i+1, curr)
	}
}
func qSort(v []int) {
	_qSort(v, 0, len(v)-1)
}

func main() {
	var v []int = []int{1, 4, 3, 2, 6, 7, 8, 5, 3, 2, 5}

	fmt.Println(v)
	naiveSort(v)
	fmt.Println(v)

	v = []int{1, 4, 3, 2, 6, 7, 8, 5, 3, 2, 5}
	fmt.Println(v)
	bSort(v)
	fmt.Println(v)

	v = []int{1, 4, 3, 2, 6, 7, 8, 5, 3, 2, 5}
	fmt.Println(v)
	selSort(v)
	fmt.Println(v)

	v = []int{1, 4, 3, 2, 6, 7, 8, 5, 3, 2, 5}
	fmt.Println(v)
	qSort(v)
	fmt.Println(v)
}
