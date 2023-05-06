run:=python -m

parse:
	$(run) lek.cmd.runner mini_c.lek test-tokens.txt | $(run) parsa
