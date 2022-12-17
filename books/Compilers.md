Compilers, Principles, Techniques, and Tools
===

> Second Edition, Alfread V. Aho et al.  
> 机械工业出版社。  

# chap1. Introduction

Language processors involve compilers and interpreters.

preprocessor, compiler, assembler, linker/loader.

The first step of a compiler's work is lexical analysis, namely scanning.
The lexical analyzer reads the stream of the source code, and organize
them into a sequence of meaningful lexeme. `< token-name, attribute-value >`.

The second step of a compiler's work is called syntax analysis or parsing.

"Environment" is a mapping from name to memory location.
"State" is a mapping from memory location to value.

# chap2. a simple syntax-directed translator

BNF paradigm.

BNF e.g. `S -> S S + | S S * | a`.

pseudo code for an predictive parser
```
void stmt() {
  switch ( lookahead ) {
  case expr:
    match(expr); match(';'); break;
  case if:
    match(if); match('(');
    optexpr(); match(';'); optexpr(); match(';'); optexpr(); match(')');
    stmt(); break;
  case other:
    match(other); break;
  default:
    report("syntax error");
  }
}

void optexpr() {
  if (lookahead == expr) match(expr);
}

void match(terminal t) {
  if (lookahead == t) lookahead = nextTerminal;
  else report("syntax error");
}
```

lexical analyzer, i.e. lexer
```
Token scan() {
  skip white spaces;
  process numbers;
  process reversed words and symbols;

  Token t = new Token(peek);
  peek = ''
  return t
}
```

```
if(peek == '\n') line = line + 1;

-> lexical analyzer ->

<if> <(> <id, peek> <eq> <const, '\n'> <)>
  <id, line> <assign> <id, line> <+> <num, 1> <;>

-> syntax-directed translator ->

...
```

# chap3. lexical analysis

pp. 68
