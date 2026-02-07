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

Declaration -> VarDecl
            | FunctionDecl
            | Statement

Type        -> "int" | "float" | "bool" | "string" | "void"

VarDecl     -> Type ID ";"

FunctionDecl -> "function" Type ID "(" Params? ")" Block

Params      -> Param ("," Param)*
Param       -> Type ID

Statement   -> IfStmt | WhileStmt | ForStmt | ReturnStmt | PrintStmt | Block | Assign | Call

IfStmt      -> "if" "(" Expr ")" Statement ("else" IfStmt | "else" Statement)?
WhileStmt   -> "while" "(" Expr ")" Statement
ForStmt     -> "for" "(" ForInit ";" Expr? ";" Expr? ")" Statement
ForInit     -> VarDeclNoSemi | AssignNoSemi | ε

ReturnStmt  -> "return" Expr? ";"
PrintStmt   -> "print" "(" Expr ")" ";"
Block       -> "{" Declaration* "}"

Assign      -> ID "=" Expr ";"
AssignNoSemi -> ID "=" Expr
Call        -> ID "(" (Expr ("," Expr)*)? ")" ";"

Expr        -> Or
Or          -> And ("||" And)*
And         -> Equality ("&&" Equality)*
Equality    -> Comparison (("==" | "!=") Comparison)*
Comparison  -> Term (("<" | "<=" | ">" | ">=") Term)*
Term        -> Factor (("+" | "-") Factor)*
Factor      -> Unary (("*" | "/") Unary)*
Unary       -> ("-" | "!") Unary | Primary
Primary     -> NUMBER | FLOAT | STRING | "true" | "false" | ID | "(" Expr ")"
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
function void main() {
  int i;
  i = 0;

  for (i = 0; i < 3; ) {
    print(i);
    i = i + 1;
  }
}
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

## ✅ Notes

This project is **fully hand‑written** and does **not** use parser generators (ANTLR/YACC/Bison).