import json

class Visitor:
    def visit_program(self, node): pass
    def visit_vardecl(self, node): pass
    def visit_funcdecl(self, node): pass
    def visit_block(self, node): pass
    def visit_if(self, node): pass
    def visit_while(self, node): pass
    def visit_return(self, node): pass
    def visit_assign(self, node): pass
    def visit_binop(self, node): pass
    def visit_unary(self, node): pass
    def visit_literal(self, node): pass
    def visit_identifier(self, node): pass
    def visit_call(self, node): pass

class PrintVisitor(Visitor):
    def __init__(self):
        self.indent = 0

    def _p(self, msg):
        print("  " * self.indent + msg)

    def _visit_list(self, nodes):
        self.indent += 1
        for n in nodes:
            n.accept(self)
        self.indent -= 1

    def visit_program(self, node):
        self._p("Program")
        self._visit_list(node.declarations)

    def visit_vardecl(self, node):
        self._p(f"VarDecl type={node.var_type} name={node.name}")

    def visit_funcdecl(self, node):
        self._p(f"FuncDecl {node.name} params={node.params}")
        self.indent += 1
        node.body.accept(self)
        self.indent -= 1

    def visit_block(self, node):
        self._p("Block")
        self._visit_list(node.statements)

    def visit_if(self, node):
        self._p("If")
        self.indent += 1
        self._p("Condition:")
        self.indent += 1
        node.condition.accept(self)
        self.indent -= 1
        self._p("Then:")
        self.indent += 1
        node.then_branch.accept(self)
        self.indent -= 1
        if node.else_branch:
            self._p("Else:")
            self.indent += 1
            node.else_branch.accept(self)
            self.indent -= 1
        self.indent -= 1

    def visit_while(self, node):
        self._p("While")
        self.indent += 1
        node.condition.accept(self)
        node.body.accept(self)
        self.indent -= 1

    def visit_return(self, node):
        self._p("Return")
        if node.value:
            self.indent += 1
            node.value.accept(self)
            self.indent -= 1

    def visit_assign(self, node):
        self._p(f"Assign {node.name}")
        self.indent += 1
        node.value.accept(self)
        self.indent -= 1

    def visit_binop(self, node):
        self._p(f"BinaryOp {node.op}")
        self.indent += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent -= 1

    def visit_unary(self, node):
        self._p(f"UnaryOp {node.op}")
        self.indent += 1
        node.operand.accept(self)
        self.indent -= 1

    def visit_literal(self, node):
        self._p(f"Literal {node.value}")

    def visit_identifier(self, node):
        self._p(f"Identifier {node.name}")

    def visit_call(self, node):
        self._p(f"Call {node.name}")
        self._visit_list(node.args)

class JsonVisitor(Visitor):
    def to_json(self, node):
        return json.dumps(node.accept(self), indent=2)

    def visit_program(self, node):
        return {"type": "Program", "declarations": [d.accept(self) for d in node.declarations]}

    def visit_vardecl(self, node):
        return {"type": "VarDecl", "var_type": node.var_type, "name": node.name}

    def visit_funcdecl(self, node):
        return {"type": "FuncDecl", "name": node.name, "params": node.params, "body": node.body.accept(self)}

    def visit_block(self, node):
        return {"type": "Block", "statements": [s.accept(self) for s in node.statements]}

    def visit_if(self, node):
        return {
            "type": "If",
            "condition": node.condition.accept(self),
            "then": node.then_branch.accept(self),
            "else": node.else_branch.accept(self) if node.else_branch else None
        }

    def visit_while(self, node):
        return {"type": "While", "condition": node.condition.accept(self), "body": node.body.accept(self)}

    def visit_return(self, node):
        return {"type": "Return", "value": node.value.accept(self) if node.value else None}

    def visit_assign(self, node):
        return {"type": "Assign", "name": node.name, "value": node.value.accept(self)}

    def visit_binop(self, node):
        return {"type": "BinaryOp", "op": node.op, "left": node.left.accept(self), "right": node.right.accept(self)}

    def visit_unary(self, node):
        return {"type": "UnaryOp", "op": node.op, "operand": node.operand.accept(self)}

    def visit_literal(self, node):
        return {"type": "Literal", "value": node.value}

    def visit_identifier(self, node):
        return {"type": "Identifier", "name": node.name}

    def visit_call(self, node):
        return {"type": "Call", "name": node.name, "args": [a.accept(self) for a in node.args]}