from ast_nodes import *
from lexer import Token

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.errors = []

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        if self.current().type != "EOF":
            self.pos += 1

    def match(self, *types):
        if self.current().type in types:
            t = self.current()
            self.pos += 1
            return t
        return None

    def expect(self, *types):
        tok = self.match(*types)
        if not tok:
            cur = self.current()
            msg = f"Expected {types} but got {cur.type} at line {cur.line}, col {cur.column}"
            self.errors.append(msg)
            self.synchronize()
            raise ParserError(msg)
        return tok

    def synchronize(self):
        # Always advance at least once to avoid infinite loops
        if self.current().type != "EOF":
            self.advance()

        sync_types = {
            "SEMICOL", "RBRACE", "EOF",
            "INT", "FUNCTION", "IF", "WHILE", "RETURN"
        }
        while self.current().type not in sync_types:
            self.advance()

        if self.current().type == "SEMICOL":
            self.advance()

    def parse(self):
        decls = []
        while self.current().type != "EOF":
            try:
                decls.append(self.declaration())
            except ParserError:
                self.synchronize()
        return Program(decls)

    def declaration(self):
        if self.match("INT"):
            name = self.expect("ID").value
            self.expect("SEMICOL")
            return VarDecl("int", name)
        if self.match("FUNCTION"):
            name = self.expect("ID").value
            self.expect("LPAREN")
            params = []
            if self.current().type == "ID":
                params.append(self.expect("ID").value)
                while self.match("COMMA"):
                    params.append(self.expect("ID").value)
            self.expect("RPAREN")
            body = self.block()
            return FuncDecl(name, params, body)
        return self.statement()

    def statement(self):
        if self.match("IF"):
            self.expect("LPAREN")
            cond = self.expression()
            self.expect("RPAREN")
            then_branch = self.statement()
            else_branch = None
            if self.match("ELSE"):
                else_branch = self.statement()
            return IfStmt(cond, then_branch, else_branch)

        if self.match("WHILE"):
            self.expect("LPAREN")
            cond = self.expression()
            self.expect("RPAREN")
            body = self.statement()
            return WhileStmt(cond, body)

        if self.match("RETURN"):
            if self.current().type != "SEMICOL":
                val = self.expression()
            else:
                val = None
            self.expect("SEMICOL")
            return ReturnStmt(val)

        if self.current().type == "LBRACE":
            return self.block()

        if self.current().type == "INT":
            self.match("INT")
            name = self.expect("ID").value
            self.expect("SEMICOL")
            return VarDecl("int", name)

        if self.current().type == "ID":
            name = self.expect("ID").value
            if self.match("OP") and self.tokens[self.pos - 1].value == "=":
                expr = self.expression()
                self.expect("SEMICOL")
                return Assign(name, expr)
            elif self.current().type == "LPAREN":
                self.expect("LPAREN")
                args = []
                if self.current().type != "RPAREN":
                    args.append(self.expression())
                    while self.match("COMMA"):
                        args.append(self.expression())
                self.expect("RPAREN")
                self.expect("SEMICOL")
                return Call(name, args)
            else:
                cur = self.current()
                msg = f"Invalid statement near {cur.type} at line {cur.line}, col {cur.column}"
                self.errors.append(msg)
                self.synchronize()
                raise ParserError(msg)

        cur = self.current()
        msg = f"Unexpected token {cur.type} at line {cur.line}, col {cur.column}"
        self.errors.append(msg)
        self.synchronize()
        raise ParserError(msg)

    def block(self):
        self.expect("LBRACE")
        stmts = []
        while self.current().type not in ("RBRACE", "EOF"):
            try:
                stmts.append(self.declaration())
            except ParserError:
                self.synchronize()
        self.expect("RBRACE")
        return Block(stmts)

    def expression(self):
        return self.equality()

    def equality(self):
        node = self.comparison()
        while self.current().type == "OP" and self.current().value in ("==", "!="):
            op = self.expect("OP").value
            right = self.comparison()
            node = BinaryOp(node, op, right)
        return node

    def comparison(self):
        node = self.term()
        while self.current().type == "OP" and self.current().value in ("<", "<=", ">", ">="):
            op = self.expect("OP").value
            right = self.term()
            node = BinaryOp(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.current().type == "OP" and self.current().value in ("+", "-"):
            op = self.expect("OP").value
            right = self.factor()
            node = BinaryOp(node, op, right)
        return node

    def factor(self):
        node = self.unary()
        while self.current().type == "OP" and self.current().value in ("*", "/"):
            op = self.expect("OP").value
            right = self.unary()
            node = BinaryOp(node, op, right)
        return node

    def unary(self):
        if self.current().type == "OP" and self.current().value in ("-", "!"):
            op = self.expect("OP").value
            right = self.unary()
            return UnaryOp(op, right)
        return self.primary()

    def primary(self):
        if self.match("NUMBER"):
            return Literal(self.tokens[self.pos - 1].value)
        if self.match("ID"):
            name = self.tokens[self.pos - 1].value
            if self.current().type == "LPAREN":
                self.expect("LPAREN")
                args = []
                if self.current().type != "RPAREN":
                    args.append(self.expression())
                    while self.match("COMMA"):
                        args.append(self.expression())
                self.expect("RPAREN")
                return Call(name, args)
            return Identifier(name)
        if self.match("LPAREN"):
            expr = self.expression()
            self.expect("RPAREN")
            return expr

        cur = self.current()
        msg = f"Unexpected token {cur.type} at line {cur.line}, col {cur.column}"
        self.errors.append(msg)
        self.synchronize()
        raise ParserError(msg)