run:=python -m
tmp_tokens:=tokens.txt

run:
	@make run-scanner SCANNER=$(SCANNER) PROGRAM=$(PROGRAM)
	@make parse

run-scanner:
	@$(run) lek.cmd.runner $(SCANNER) $(PROGRAM) > $(tmp_tokens)


mini_c_example:
	@make run SCANNER=examples/mini_c.lek PROGRAM=examples/test-program.txt

parse:
	@$(run) parsa $(tmp_tokens)

scanner:
	@$(run) lek.cmd.generator $(SPEC) $(OUT)

test:
	pytest tests