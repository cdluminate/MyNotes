chart:
	sh chart.sh
	octave chart.m

main:
	g++ main.cc -O2 -march=native -ftree-vectorize -funroll-loops -lmkl_rt
	./a.out 2>&1 | tee result

.PHONY: t
t:
	g++ -O2 -march=native t.cc gemm1.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm2.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm3.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm4.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm5.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm6.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm7.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm8.c -o t -lblas; ./t
	g++ -O2 -march=native t.cc gemm9.c -o t -lblas; ./t
