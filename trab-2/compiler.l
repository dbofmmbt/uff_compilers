%{
#include "compiler.tab.h"
%}

%%
"+"    { return ADD; }
"-"    { return SUB; }
"*"    { return MUL; }
"/"    { return DIV; }
[0-9]+ { yylval = atoi(yytext); return NUMBER; }
\n     { return NEWLINE; }
[ \t]  { }
.      { printf("Mystery character %s\n", yytext); }
%%

