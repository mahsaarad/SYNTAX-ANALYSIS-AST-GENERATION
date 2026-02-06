from dataclasses import dataclass
from typing import List, Optional, Any

class Node:
    def accept(self, visitor):
        raise NotImplementedError()

@dataclass
class Program(Node):
    declarations: List[Node]
    def accept(self, visitor): return visitor.visit_program(self)

@dataclass
class VarDecl(Node):
    var_type: str
    name: str
    def accept(self, visitor): return visitor.visit_vardecl(self)

@dataclass
class FuncDecl(Node):
    name: str
    params: List[str]
    body: 'Block'
    def accept(self, visitor): return visitor.visit_funcdecl(self)

@dataclass
class Block(Node):
    statements: List[Node]
    def accept(self, visitor): return visitor.visit_block(self)

@dataclass
class IfStmt(Node):
    condition: Node
    then_branch: Node
    else_branch: Optional[Node]
    def accept(self, visitor): return visitor.visit_if(self)

@dataclass
class WhileStmt(Node):
    condition: Node
    body: Node
    def accept(self, visitor): return visitor.visit_while(self)

@dataclass
class ReturnStmt(Node):
    value: Optional[Node]
    def accept(self, visitor): return visitor.visit_return(self)

@dataclass
class Assign(Node):
    name: str
    value: Node
    def accept(self, visitor): return visitor.visit_assign(self)

@dataclass
class BinaryOp(Node):
    left: Node
    op: str
    right: Node
    def accept(self, visitor): return visitor.visit_binop(self)

@dataclass
class Literal(Node):
    value: str
    def accept(self, visitor): return visitor.visit_literal(self)

@dataclass
class Identifier(Node):
    name: str
    def accept(self, visitor): return visitor.visit_identifier(self)

@dataclass
class Call(Node):
    name: str
    args: List[Node]
    def accept(self, visitor): return visitor.visit_call(self)