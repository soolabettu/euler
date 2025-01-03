package main

import "fmt"

func main() {
	var sum int = 1
	for i := 3; i <= 1001; i += 2 {
		x := i - 1
		square := i * i
		sum += square - 0 + square - x + square - 2 * x + square - 3 * x
    }

	fmt.Println(sum)
}