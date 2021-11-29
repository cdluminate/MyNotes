package main

import (
	"fmt"
)

// Sequential Search
func seqSearch(v []int, target int) int {
	if len(v) == 0 {
		return -1
	}
	for i, vi := range v {
		if vi == target {
			return i
		}
	}
	return -1
}

// BiSearch
func biSearch(v []int, target int) int {
	if len(v) == 0 {
		return -1
	}
	curl, curr := 0, len(v)-1
	for curl <= curr {
		curm := (curl + curr) / 2
		if v[curm] == target {
			return curm
		} else if v[curm] > target {
			curr = curm - 1
		} else { // v[curm] < target
			curl = curm + 1
		}
	}
	return -1
}

func main() {
	var v []int = []int{1, 2, 3, 4, 5, 6, 7, 8}
	fmt.Println(seqSearch(v, 1), seqSearch(v, 8), seqSearch(v, 100))
	fmt.Println(biSearch(v, 1), biSearch(v, 8), biSearch(v, 100))
}
