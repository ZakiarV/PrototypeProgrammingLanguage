from src.LexicalAnalysis.lexer import Lexer
from src.SyntaxAnalysis.parser import Parser
from src.SemanticsAnalysis.semantics_analysis import SemanticsAnalysis
from src.Translator.translator import Translator
from src.Compiler.compile import Compiler


def main():
    with open("UserCode/main.ppl") as f:
        source_code = f.read()

    lexer = Lexer(source_code)
    parser = Parser(lexer.tokenize())
    semantics_analysis = SemanticsAnalysis(parser.parse())
    type_tree = semantics_analysis.analyze()
    translator = Translator(type_tree, semantics_analysis.symbol_table)
    translator.translate()
    compiler = Compiler()
    compiler.compile()

if __name__ == "__main__":
    main()