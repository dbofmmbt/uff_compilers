run:=python -m

parse:
	$(run) lek.cmd.runner mini_c.lek parsa_test_input.txt | $(run) parsa
