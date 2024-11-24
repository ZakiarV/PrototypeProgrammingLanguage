from src.LexicalAnalysis.lexer import Lexer
from src.SyntaxAnalysis.parser import Parser


def main():
    with open("UserCode/main.ppl") as f:
        source_code = f.read()

    lexer = Lexer(source_code)
    parser = Parser(lexer.tokenize())
    print(parser.parse())



if __name__ == "__main__":
    main()