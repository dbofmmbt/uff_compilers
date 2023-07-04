run: compiler.l compiler.y
	bison -d compiler.y
	flex compiler.l
	cc -o $@.out compiler.tab.c lex.yy.c -lfl