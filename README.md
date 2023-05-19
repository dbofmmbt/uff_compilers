# Trabalho de Compiladores

O trabalho foi desenvolvido usando Python 3.11. Além disso, foi usado `graphviz` para gerar visualização de grafos e `pytest` para execução de testes.

Com `make mini_c_example` é possível rodar um exemplo completo de um programa Mini C, que está [aqui](examples/test-program.txt).

`make test` roda os testes que foram implementados dentro da pasta `tests`. Eles verificam o scanner generator.

`make run` pode ser usado para tokenizar e parsear um programa. e.g. `make run SCANNER=examples/mini_c.lek PROGRAM=examples/test-if.txt`.

No arquivo [mini_c_lek_input.txt](examples/mini_c_lek_input.txt) está a especificação de tokens de mini c usada.

No arquivo [ready_for_parsa.txt](parsa/mini_c_grammar/ready_for_parsa.txt) está a BNF usada pelo parser.
