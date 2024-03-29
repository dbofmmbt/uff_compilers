%{
#include "compiler.tab.h"
%}

%%
"int"  { return INT; }
"float"  { return FLOAT; }
"char"  { return CHAR; }
"for"  { return FOR; }
"while" { return WHILE; }
"if"   { return IF; }
"else" { return ELSE; }
"goto" { return GOTO; }
"+"    { return ADD; }
"-"    { return SUB; }
"*"    { return MUL; }
"/"    { return DIV; }
"="    { return ASSIGN; }
"=="   { return EQ; }
"!="   { return DIF; }
"<"    { return LT; }
">"    { return GT; }
"<="   { return LE; }
">="   { return GE; }
","    { return COMMA; }
";"    { return SEMICOLON; }
"("    { return PAREN_LEFT; }
")"    { return PAREN_RIGHT; }
"{"    { return CURLY_LEFT; }
"}"    { return CURLY_RIGHT; }
\:[a-z]* { yylval.str = strdup(yytext); return LABEL; }
[0-9]+ { yylval.str = strdup(yytext); return NUMBER; }
[a-zA-Z][a-zA-Z0-9]* { yylval.str = strdup(yytext); return ID; } // TODO save identifier in symbol table
[ \t \n]  { }
%%

