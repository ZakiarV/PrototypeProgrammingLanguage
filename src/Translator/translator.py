from src.Tokens.token_types import TokenTypes

from src.SemanticsAnalysis.types_f.type_node import TypeBinaryOperationNode
from src.SemanticsAnalysis.types_f.type_node import TypeValueNode
from src.SemanticsAnalysis.types_f.type_node import TypeFunctionDeclaration
from src.SemanticsAnalysis.types_f.type_node import TypeMethodDeclaration
from src.SemanticsAnalysis.types_f.type_node import TypeReturnStatement
from src.SemanticsAnalysis.types_f.type_node import TypeVariableDeclaration
from src.SemanticsAnalysis.types_f.type_node import TypeVariableAssignment
from src.SemanticsAnalysis.types_f.type_node import TypeFunctionCall
from src.SemanticsAnalysis.types_f.type_node import TypeFieldAccess
from src.SemanticsAnalysis.types_f.type_node import TypeMethodCall
from src.SemanticsAnalysis.types_f.type_node import TypeClassConstructor
from src.SemanticsAnalysis.types_f.type_node import TypeClassInstantiation
from src.SemanticsAnalysis.types_f.type_node import TypeFieldDeclaration
from src.SemanticsAnalysis.types_f.type_node import TypeIfStatement
from src.SemanticsAnalysis.types_f.type_node import TypeForStatement
from src.SemanticsAnalysis.types_f.type_node import TypeWhileStatement

from src.SyntaxAnalysis.nodes import ProgramNode
from src.SyntaxAnalysis.nodes import ClassDeclaration


class Translator:
    def __init__(self, type_tree, symbol_table):
        self.type_tree = type_tree
        self.symbol_table = symbol_table
        self.token_types = TokenTypes()
        self.errors = []
        self.translated = []

    def translate(self):
        pass