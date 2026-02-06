# Recursive Descent Parser + AST + Visitor (Python)

This project implements a **hand-written recursive descent parser** for a small language subset, builds an **AST**, and prints the tree using the **Visitor pattern**. It also supports **JSON output** and **error recovery**.

---

## ✅ Features
- Hand‑written **recursive descent parser**
- **AST construction** (Program, Functions, Statements, Expressions, etc.)
- **Visitor pattern** for tree traversal
- **PrintVisitor** (pretty AST output)
- **JsonVisitor** (JSON AST output)
- **Error recovery** (keeps parsing after syntax errors)
- Supports variable declarations inside blocks

---

## ✅ Grammar (summary)

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

## ✅ Project Structure

```
.
├── ast_nodes.py
├── lexer.py
├── parser.py
├── visitor.py
├── main.py
├── grammar.txt
└── tests/
    ├── input1_valid.txt
    ├── input2_nested.txt
    ├── input3_invalid.txt
    └── input4.txt
```

---

## ✅ Run (Windows / WSL / Linux)

```bash
python main.py tests/input1_valid.txt
```

For JSON output:

```bash
python main.py tests/input1_valid.txt --json
```

---

## ✅ Example Input

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

## ✅ Example Output (PrintVisitor)

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

## ✅ Error Recovery
If the input contains invalid syntax, the parser:
- reports errors,
- skips to a safe point,
- continues parsing.

---

## ✅ Requirements
- Python 3.8+

---

## ✅ Notes
This project is **hand‑written** and does **not** use parser generators (ANTLR/YACC/Bison), as required by the assignment.
