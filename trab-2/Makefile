run: compiler.l compiler.y
	bison -d compiler.y
	flex compiler.l
	cc -g -o $@.out **.c -lfl
	./$@.out test-program.txt