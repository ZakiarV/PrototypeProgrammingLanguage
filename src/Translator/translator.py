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
from src.SemanticsAnalysis.types_f.type_node import TypeIfStatement
from src.SemanticsAnalysis.types_f.type_node import TypeForStatement
from src.SemanticsAnalysis.types_f.type_node import TypeWhileStatement

from src.SyntaxAnalysis.nodes import ProgramNode
from src.SyntaxAnalysis.nodes import ClassDeclaration

from .c_code.get_c_code_directory import get_c_code_directory


class Translator:
    def __init__(self, type_tree, symbol_table):
        self.type_tree = type_tree
        self.symbol_table = symbol_table
        self.token_types = TokenTypes()
        self.errors = []
        self.translated = []

    def translate(self):
        self.translate_program(self.type_tree)
        if len(self.errors) > 0:
            return self.errors
        else:
            with open(f"{get_c_code_directory()}/main.cpp", "w") as file:
                file.write("\n".join(self.translated))

    def translate_program(self, program):
        self.translated.append("#include <iostream>")
        self.translated.append("#include <string>")
        self.translated.append("#include \"std_lib.h\"")
        self.translated.append("using namespace std;")
        self.translated.append("")
        if isinstance(program, ProgramNode):
            for i in range(len(program.body_ast)):
                if isinstance(program.body_ast[i], ClassDeclaration):
                    self.translate_class_declaration(program.body_ast[i])
                elif isinstance(program.body_ast[i], TypeFunctionDeclaration):
                    self.translate_function_declaration(program.body_ast[i])
            for node in program.body_ast:
                if isinstance(node, ClassDeclaration):
                    program.body_ast.remove(node)
                elif isinstance(node, TypeFunctionDeclaration):
                    program.body_ast.remove(node)
            self.translated.append("int main() {")
            if len(program.body_ast) > 0:
                for i in range(len(program.body_ast)):
                    self.translate_node(program.body_ast[i])
            self.translated.append("\treturn 0;")
            self.translated.append("}")

    def translate_class_declaration(self, class_declaration: ClassDeclaration):
        self.translated.append(f"typedef struct {class_declaration.class_name} {{")
        if len(self.symbol_table.class_declarations[class_declaration.class_name].fields) > 0:
            for field in self.symbol_table.class_declarations[class_declaration.class_name].fields.items():
                self.translated.append(f"\t{field[1].lower()} {field[0]};")
        if class_declaration.constructor is not None:
            self.translate_class_constructor(class_declaration.constructor)
        if len(class_declaration.methods) > 0:
            for method in class_declaration.methods:
                self.translate_method_declaration(method)
        self.translated.append(f"}} {class_declaration.class_name};")

    def translate_class_constructor(self, constructor: TypeClassConstructor):
        self.translated.append(f"\tvoid init({",".join([f"{parameter.variable_type.lower()} {parameter.variable_name}" for parameter in constructor.parameters])}) {{")
        for i in range(len(constructor.body)):
            if isinstance(constructor.body[i], TypeVariableDeclaration):
                self.translate_constructor_variable_declaration(constructor.body[i])
            else:
                self.translate_node(constructor.body[i], 2)
        self.translated.append("\t}")

    def translate_constructor_variable_declaration(self, node: TypeVariableDeclaration):
        self.translated.append(f"\t\t{node.variable_name} = {self.translate_node(node.initialization_type)};")

    def translate_method_declaration(self, method: TypeMethodDeclaration):
        if not method.type:
            self.translated.append(f"\tvoid {method.method_name}({",".join([f"{parameter.variable_type.lower()} {parameter.variable_name}" for parameter in method.parameters])}) {{")
        else:
            self.translated.append(f"\t{method.type.lower()} {method.method_name}({",".join([f"{parameter.variable_type.lower()} {parameter.variable_name}" for parameter in method.parameters])}) {{")
        for i in range(len(method.body)):
            if isinstance(method.body[i], TypeVariableDeclaration):
                self.translate_method_variable_declaration(method.body[i])
            else:
                self.translate_node(method.body[i], 2)
        self.translated.append("\t}")

    def translate_method_variable_declaration(self, node: TypeVariableDeclaration):
        self.translated.append(f"\t\t{node.variable_type.lower()} {node.variable_name} = {self.translate_node(node.initialization_type)};")

    def translate_function_declaration(self, function_declaration: TypeFunctionDeclaration):
        if not function_declaration.type:
            self.translated.append(f"void {function_declaration.function_name}({",".join([f"{parameter.variable_type.lower()} {parameter.variable_name}" for parameter in function_declaration.parameters])}) {{")
        else:
            self.translated.append(f"{function_declaration.type.lower()} {function_declaration.function_name}({",".join([f"{parameter.variable_type.lower()} {parameter.variable_name}" for parameter in function_declaration.parameters])}) {{")
        for i in range(len(function_declaration.body)):
            self.translate_node(function_declaration.body[i], 1)
        self.translated.append("}")

    def translate_node(self, node, recursion_level=1, is_assignment=False, is_for_loop=False):
        if isinstance(node, TypeWhileStatement):
            self.translate_while_statement(node, recursion_level)
        elif isinstance(node, TypeBinaryOperationNode):
            return self.translate_binary_operation(node, recursion_level)
        elif isinstance(node, TypeValueNode):
            return node.node.token.value
        elif isinstance(node, TypeVariableDeclaration):
            if is_for_loop:
                return self.translate_variable_declaration(node, recursion_level, is_for_loop=is_for_loop)
            else:
                self.translate_variable_declaration(node, recursion_level, is_for_loop=is_for_loop)
        elif isinstance(node, TypeVariableAssignment):
            if is_for_loop:
                return self.translate_variable_assignment(node, recursion_level, is_for_loop=is_for_loop)
            else:
                self.translate_variable_assignment(node, recursion_level, is_for_loop=is_for_loop)
        elif isinstance(node, TypeFunctionCall):
            if is_assignment:
                return self.translate_function_call(node, recursion_level, is_assignment)
            else:
                self.translate_function_call(node, recursion_level, is_assignment)
        elif isinstance(node, TypeReturnStatement):
            pass
        elif isinstance(node, TypeFieldAccess):
            pass
        elif isinstance(node, TypeMethodCall):
            if is_assignment:
                return self.translate_method_call(node, recursion_level, is_assignment)
            else:
                self.translate_method_call(node, recursion_level, is_assignment)
        elif isinstance(node, TypeIfStatement):
            self.translate_if_statement(node, recursion_level)
        elif isinstance(node, TypeForStatement):
            self.translate_for_statement(node, recursion_level)

    def translate_while_statement(self, node: TypeWhileStatement, recursion_level):
        self.translated.append(f"{"\t" * recursion_level}while ({self.translate_node(node.condition)}) {{")
        for i in range(len(node.body)):
            self.translate_node(node.body[i], recursion_level + 1)
        self.translated.append(f"{"\t" * recursion_level}}}")

    def translate_binary_operation(self, node: TypeBinaryOperationNode, recursion_level):
        if node.operator == self.token_types.PLUS:
            return f"{self.translate_node(node.type_left)} + {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.MINUS:
            return f"{self.translate_node(node.type_left)} - {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.MUL:
            return f"{self.translate_node(node.type_left)} * {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.DIV:
            return f"{self.translate_node(node.type_left)} / {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.MOD:
            return f"{self.translate_node(node.type_left)} % {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.EQ:
            return f"{self.translate_node(node.type_left)} == {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.NEQ:
            return f"{self.translate_node(node.type_left)}!= {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.GT:
            return f"{self.translate_node(node.type_left)} > {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.GTE:
            return f"{self.translate_node(node.type_left)} >= {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.LT:
            return f"{self.translate_node(node.type_left)} < {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.LTE:
            return f"{self.translate_node(node.type_left)} <= {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.AND:
            return f"{self.translate_node(node.type_left)} && {self.translate_node(node.type_right)}"
        elif node.operator == self.token_types.OR:
            return f"{self.translate_node(node.type_left)} || {self.translate_node(node.type_right)}"

    def translate_variable_declaration(self, node: TypeVariableDeclaration, recursion_level, is_for_loop=False):
        if node.variable_type in [self.token_types.INT, self.token_types.FLOAT, self.token_types.STRING, self.token_types.BOOLEAN]:
            if is_for_loop:
                return f"{node.variable_type.lower()} {node.variable_name} = {self.translate_node(node.initialization_type, is_assignment=True)}"
            else:
                self.translated.append(f"{"\t" * recursion_level}{node.variable_type.lower()} {node.variable_name} = {self.translate_node(node.initialization_type, is_assignment=True)};")
        elif node.variable_type in self.symbol_table.class_declarations.keys():
            self.translated.append(f"{"\t" * recursion_level}{node.variable_type} {node.variable_name};")
            self.translated.append(f"{"\t" * recursion_level}{node.variable_name}.init({", ".join([self.translate_node(argument) for argument in node.initialization_type.arguments])});")
        else:
            self.translated.append(f"{"\t" * recursion_level}{node.variable_type} {node.variable_name} = {self.translate_node(node.initialization_type, is_assignment=True)};")

    def translate_variable_assignment(self, node: TypeVariableAssignment, recursion_level, is_for_loop=False):
        if is_for_loop:
            return f"{node.variable_name} = {self.translate_node(node.assignment_type, is_assignment=True)}"
        else:
            self.translated.append(f"{"\t" * recursion_level}{node.variable_name} = {self.translate_node(node.assignment_type, is_assignment=True)};")

    def translate_function_call(self, node: TypeFunctionCall, recursion_level, is_assignment=False):
        if is_assignment:
            if node.function_name == "input":
                if node.arguments[0].node.token.type == self.token_types.STRING:
                    return f"input(\"{self.translate_node(node.arguments[0])}\")"
                return f"input({self.translate_node(node.arguments[0])})"
            elif node.function_name == "int":
                if node.arguments[0].node.token.type == self.token_types.STRING:
                    return f"icasts(\"{self.translate_node(node.arguments[0])}\")"
                return f"scasti({", ".join([self.translate_node(argument) for argument in node.arguments])})"
            elif node.function_name == "str":
                return f"icasts({", ".join([self.translate_node(argument) for argument in node.arguments])})"
            else:
                return f"{node.function_name}({", ".join([self.translate_node(argument) for argument in node.arguments])})"
        else:
            if node.function_name == "print":
                if node.arguments[0].node.token.type == self.token_types.STRING:
                    self.translated.append(f"{"\t" * recursion_level}print(\"{self.translate_node(node.arguments[0])}\");")
                else:
                    self.translated.append(f"{"\t" * recursion_level}print({self.translate_node(node.arguments[0])});")
            elif node.function_name == "wait":
                self.translated.append(f"{"\t" * recursion_level}wait({node.node.arguments[0].token.value});")
            else:
                self.translated.append(f"{"\t" * recursion_level}{node.function_name}({", ".join([self.translate_node(argument) for argument in node.arguments])});")

    def translate_method_call(self, node: TypeMethodCall, recursion_level, is_assignment=False):
        if is_assignment:
            return f"{node.class_name}.{node.method_name}({", ".join([self.translate_node(argument) for argument in node.arguments])})"
        else:
            self.translated.append(f"{"\t" * recursion_level}{node.class_name}.{node.method_name}({", ".join([self.translate_node(argument) for argument in node.arguments])});")

    def translate_if_statement(self, node: TypeIfStatement, recursion_level):
        self.translated.append(f"{"\t" * recursion_level}if ({self.translate_node(node.condition)}) {{")
        for i in range(len(node.body)):
            self.translate_node(node.body[i], recursion_level + 1)
        self.translated.append(f"{"\t" * recursion_level}}}")
        if len(node.else_body) > 0:
            self.translated.append(f"{"\t" * recursion_level}else {{")
            for i in range(len(node.else_body)):
                self.translate_node(node.else_body[i], recursion_level + 1)
            self.translated.append(f"{"\t" * recursion_level}}}")

    def translate_for_statement(self, node: TypeForStatement, recursion_level):
        self.translated.append(f"{"\t" * recursion_level}for ({self.translate_variable_declaration(node.variable, 0, is_for_loop=True)}; {self.translate_node(node.condition)}; {self.translate_variable_assignment(node.increment, 0, is_for_loop=True)}) {{")
        for i in range(len(node.body)):
            self.translate_node(node.body[i], recursion_level + 1)
        self.translated.append(f"{"\t" * recursion_level}}}")
