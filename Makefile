run:=python -m
tmp_tokens:=tokens.txt

run:
	@make run-scanner SCANNER=$(SCANNER) PROGRAM=$(PROGRAM)
	@make parse

run-scanner:
	@$(run) lek.cmd.runner $(SCANNER) $(PROGRAM) > $(tmp_tokens)


mini_c:=make run SCANNER=examples/mini_c.lek

mini_c_example:
	@$(mini_c) PROGRAM=examples/test-program.txt

mini_c_errors:
	@$(mini_c) PROGRAM=examples/test-errors.txt

mini_c_if:
	@$(mini_c) PROGRAM=examples/test-if.txt

parse:
	@$(run) parsa $(tmp_tokens)

scanner:
	@$(run) lek.cmd.generator $(SPEC) $(OUT)

test:
	pytest tests