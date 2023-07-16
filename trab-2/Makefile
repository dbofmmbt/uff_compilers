run: compiler.l compiler.y
	bison -d compiler.y
	flex compiler.l
	cc -o $@.out **.c -lfl
	./$@.out test-program.txt