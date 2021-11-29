package main

import "fmt"

func twoSum(nums []int, target int) []int {
	m := map[int]int{}
	for k, v := range nums {
		if idx, ok := m[target-v]; !ok {
			m[v] = k
		} else {
			return []int{k, idx}
		}
	}
	return []int{-1, -1}
}

func main() {
	v := []int{3, 2, 4}
	fmt.Println(twoSum(v, 6))
	v = []int{2, 7, 11, 15}
	fmt.Println(twoSum(v, 13))
}
