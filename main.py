from src.LexicalAnalysis.lexer import Lexer


def main():
    with open("UserCode/main.ppl") as f:
        source_code = f.read()

    lexer = Lexer(source_code)
    lexer.tokenize()


if __name__ == "__main__":
    main()