# Recursive Descent Parser + AST + Visitor (Python)

A hand‑written recursive descent parser for a small imperative language.  
It builds an **Abstract Syntax Tree (AST)** and prints it using the **Visitor Design Pattern**.  
JSON output and syntax error recovery are supported.

---

##  Features

- **Recursive descent parser** (no parser generators)
- **AST construction** (Program, Functions, Statements, Expressions)
- **Visitor pattern** for AST traversal
- **PrintVisitor** (pretty tree output)
- **JsonVisitor** (structured JSON output)
- **Syntax error recovery** (continues parsing after errors)
- Variable declarations inside blocks

---

##  Grammar (Summary)

```
Program     -> Declaration*
Declaration -> "int" ID ";" 
            | "function" ID "(" Params? ")" Block
            | Statement

Params      -> ID ("," ID)*

Statement   -> IfStmt | WhileStmt | ReturnStmt | Block | Assign | Call

IfStmt      -> "if" "(" Expr ")" Statement ("else" Statement)?
WhileStmt   -> "while" "(" Expr ")" Statement
ReturnStmt  -> "return" Expr? ";"
Block       -> "{" Declaration* "}"

Assign      -> ID "=" Expr ";"
Call        -> ID "(" (Expr ("," Expr)*)? ")" ";"

Expr        -> Equality
Equality    -> Comparison (("==" | "!=") Comparison)*
Comparison  -> Term (("<" | "<=" | ">" | ">=") Term)*
Term        -> Factor (("+" | "-") Factor)*
Factor      -> Unary (("*" | "/") Unary)*
Unary       -> ("-" | "!") Unary | Primary
Primary     -> NUMBER | ID | "(" Expr ")"
```

---

##  Project Structure

```
.
├── ast_nodes.py
├── lexer.py
├── parser.py
├── visitor.py
├── main.py
├── grammar.txt
├── test1.txt
├── test2.txt
├── test3.txt
├── test4.txt
├── test5.txt
└── test6.txt
```

---

##  Run

### Print AST (default)
```bash
python main.py test1.txt
```

### JSON Output
```bash
python main.py test1.txt --json
```

---

##  Example Input

```text
int globalCount;

function inc(x) {
  int y;
  y = x + 1;
  return y;
}

function main() {
  int a;
  a = 5;
  a = inc(a);
}
```

---

##  Example Output (PrintVisitor)

```
Program
  VarDecl type=int name=globalCount
  FuncDecl inc params=['x']
    Block
      VarDecl type=int name=y
      Assign y
        BinaryOp +
          Identifier x
          Literal 1
      Return
        Identifier y
  FuncDecl main params=[]
    Block
      VarDecl type=int name=a
      Assign a
        Literal 5
      Assign a
        Call inc
          Identifier a
```

---

##  Error Recovery

If invalid syntax is found, the parser:

- reports the error with line/column
- skips to a safe point
- continues parsing

Example:
```
SYNTAX ERRORS:
- Expected ('SEMICOL',) but got ID at line 3, col 3
```

---

##  Requirements

- Python 3.8+

---

##  Notes

This project is **fully hand‑written** and does **not** use parser generators (ANTLR/YACC/Bison).