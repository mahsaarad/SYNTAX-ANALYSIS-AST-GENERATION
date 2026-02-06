from lexer import tokenize
from parser import Parser
from visitor import PrintVisitor, JsonVisitor

def run(code: str, json_output: bool = False):
    tokens = list(tokenize(code))
    parser = Parser(tokens)
    ast = parser.parse()

    if parser.errors:
        print("SYNTAX ERRORS:")
        for e in parser.errors:
            print("-", e)

    if json_output:
        visitor = JsonVisitor()
        print(visitor.to_json(ast))
    else:
        visitor = PrintVisitor()
        ast.accept(visitor)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <input_file> [--json]")
        sys.exit(1)

    json_output = "--json" in sys.argv
    file_arg = sys.argv[1]

    with open(file_arg, "r") as f:
        code = f.read()
    run(code, json_output=json_output)