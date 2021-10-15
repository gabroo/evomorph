package main

import (
	"fmt"
	"runtime"
  "evomorph"
)
func main() {
	pc, file, line, ok := runtime.Caller(1)
	if !ok {
		fmt.Println("Error in runtime.Caller()")
		return
	}

	fmt.Printf("Called from %s, line #%d, func: %v\n", file, line, runtime.FuncForPC(pc).Name())
	fmt.Printf("Hello world!\n")

	s := evomorph.Simulation{Id: 42, Name: "game of life"}
	fmt.Println("name: ", s.Name)
	fmt.Printf("%+v\n", s)
}
