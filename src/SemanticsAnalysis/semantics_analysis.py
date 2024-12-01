from src.SemanticsAnalysis.symbol_table.symbol_table_generator import SymbolTableGenerator
from .types_f.type_ast import TypeAST
from .types_f.type_checker import TypeChecker


class SemanticsAnalysis:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTableGenerator(ast).generate()
        self.type_ast = TypeAST(ast, self.symbol_table).analyze()


    def analyze(self):
        checked: TypeChecker = TypeChecker(self.type_ast, self.symbol_table)
        if checked.check():
            print("Semantic analysis successful")
            return self.type_ast
        else:
            print("Semantic analysis failed")
            for error in checked.errors:
                print(error)
            return None
