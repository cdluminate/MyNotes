package main

import "fmt"

func singleNumber(nums []int) int {
	var ret int = 0
	for _, v := range nums {
		ret ^= v
	}
	return ret
}

func main() {
	a := []int{1, 1, 2, 3, 3}
	b := []int{1, 2, 3, 4, 5, 5, 4, 3, 2}

	fmt.Println(singleNumber(a))
	fmt.Println(singleNumber(b))
}
