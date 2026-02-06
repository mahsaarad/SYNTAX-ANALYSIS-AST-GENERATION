import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

class LexerError(Exception):
    pass

TOKEN_SPEC = [
    ("NUMBER",   r"\d+"),
    ("ID",       r"[A-Za-z_]\w*"),
    ("OP",       r"==|!=|<=|>=|\+|-|\*|/|=|<|>"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("SEMICOL",  r";"),
    ("COMMA",    r","),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
    ("MISMATCH", r"."),
]

KEYWORDS = {
    "int", "if", "else", "while", "return", "function"
}

TOK_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
MASTER = re.compile(TOK_REGEX)

def tokenize(code: str):
    line_num = 1
    line_start = 0
    for mo in MASTER.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        if kind == "NEWLINE":
            line_num += 1
            line_start = mo.end()
            continue
        if kind == "SKIP":
            continue
        if kind == "MISMATCH":
            raise LexerError(f"Unexpected character {value!r} at line {line_num}, col {column}")

        if kind == "ID" and value in KEYWORDS:
            kind = value.upper()

        yield Token(kind, value, line_num, column)

    yield Token("EOF", "", line_num, 0)