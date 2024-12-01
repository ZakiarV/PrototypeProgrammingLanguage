from src.Tokens.token_types import TokenTypes

from .type_node import TypeBinaryOperationNode
from .type_node import TypeValueNode
from .type_node import TypeFunctionDeclaration
from .type_node import TypeMethodDeclaration
from .type_node import TypeReturnStatement
from .type_node import TypeVariableDeclaration
from .type_node import TypeVariableAssignment
from .type_node import TypeFunctionCall
from .type_node import TypeFieldAccess
from .type_node import TypeMethodCall
from .type_node import TypeClassConstructor
from .type_node import TypeClassInstantiation
from .type_node import TypeFieldDeclaration
from .type_node import TypeIfStatement
from .type_node import TypeForStatement
from .type_node import TypeWhileStatement

from src.SyntaxAnalysis.nodes import ProgramNode
from src.SyntaxAnalysis.nodes import ClassDeclaration


class TypeChecker:
    def __init__(self, type_tree, symbol_table):
        self.type_tree = type_tree
        self.symbol_table = symbol_table
        self.token_types = TokenTypes()
        self.errors = []

    def check(self):
        return self.check_program()

    def check_program(self):
        checked = self.check_node(self.type_tree)
        if not checked:
            self.errors.append("Error in program")
        return checked

    def check_node(self, node):
        if isinstance(node, ProgramNode):
            return self.check_program_node(node)
        elif isinstance(node, ClassDeclaration):
            return self.check_class_declaration_node(node)
        elif isinstance(node, TypeBinaryOperationNode):
            return self.check_type_binary_operation_node(node)
        elif isinstance(node, TypeValueNode):
            return self.check_type_value_node(node)
        elif isinstance(node, TypeFunctionDeclaration):
            return self.check_type_function_declaration_node(node)
        elif isinstance(node, TypeMethodDeclaration):
            return self.check_type_method_declaration_node(node)
        elif isinstance(node, TypeReturnStatement):
            return self.check_type_return_statement_node(node)
        elif isinstance(node, TypeVariableDeclaration):
            return self.check_type_variable_declaration_node(node)
        elif isinstance(node, TypeVariableAssignment):
            return self.check_type_variable_assignment_node(node)
        elif isinstance(node, TypeFunctionCall):
            return self.check_type_function_call_node(node)
        elif isinstance(node, TypeFieldAccess):
            return self.check_type_field_access_node(node)
        elif isinstance(node, TypeMethodCall):
            return self.check_type_method_call_node(node)
        elif isinstance(node, TypeClassConstructor):
            return self.check_type_class_constructor_node(node)
        elif isinstance(node, TypeClassInstantiation):
            return self.check_type_class_instantiation_node(node)
        elif isinstance(node, TypeFieldDeclaration):
            return self.check_type_field_declaration_node(node)
        elif isinstance(node, TypeIfStatement):
            return self.check_type_if_statement_node(node)
        elif isinstance(node, TypeForStatement):
            return self.check_type_for_statement_node(node)
        elif isinstance(node, TypeWhileStatement):
            return self.check_type_while_statement_node(node)
        else:
            raise ValueError(f"Unknown node type: {type(node).__name__}")

    def check_program_node(self, node):
        body_checked = [self.check_node(child) for child in node.body_ast]
        return all(body_checked)

    def check_class_declaration_node(self, node):
        fields_checked = all(self.check_node(child) for child in node.fields)
        methods_checked = all(self.check_node(child) for child in node.methods)
        constructor_checked = self.check_node(node.constructor) if node.constructor else True
        return fields_checked and methods_checked and (constructor_checked == node.class_name)

    def check_type_binary_operation_node(self, node: TypeBinaryOperationNode):
        if isinstance(node.type_left, str) and isinstance(node.type_right, str):
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if node.type_left == self.token_types.STRING or node.type_right == self.token_types.STRING:
                    return self.token_types.STRING
                elif node.type_left == self.token_types.FLOAT or node.type_right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif node.type_left == self.token_types.INT and node.type_right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, str) and isinstance(node.type_right, TypeValueNode):
            right = self.check_type_value_node(node.type_right)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if node.type_left == self.token_types.STRING or right == self.token_types.STRING:
                    return self.token_types.STRING
                elif node.type_left == self.token_types.FLOAT or right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif node.type_left == self.token_types.INT and right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, TypeValueNode) and isinstance(node.type_right, str):
            left = self.check_type_value_node(node.type_left)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if left == self.token_types.STRING or node.type_right == self.token_types.STRING:
                    return self.token_types.STRING
                elif left == self.token_types.FLOAT or node.type_right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif left == self.token_types.INT and node.type_right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, TypeValueNode) and isinstance(node.type_right, TypeValueNode):
            left = self.check_type_value_node(node.type_left)
            right = self.check_type_value_node(node.type_right)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if left == self.token_types.STRING or right == self.token_types.STRING:
                    return self.token_types.STRING
                elif left == self.token_types.FLOAT or right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif left == self.token_types.INT and right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, str) and isinstance(node.type_right, TypeBinaryOperationNode):
            right = self.check_type_binary_operation_node(node.type_right)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if node.type_left == self.token_types.STRING or right == self.token_types.STRING:
                    return self.token_types.STRING
                elif node.type_left == self.token_types.FLOAT or right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif node.type_left == self.token_types.INT and right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, TypeBinaryOperationNode) and isinstance(node.type_right, str):
            left = self.check_type_binary_operation_node(node.type_left)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if left == self.token_types.STRING or node.type_right == self.token_types.STRING:
                    return self.token_types.STRING
                elif left == self.token_types.FLOAT or node.type_right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif left == self.token_types.INT and node.type_right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, TypeBinaryOperationNode) and isinstance(node.type_right, TypeBinaryOperationNode):
            left = self.check_node(node.type_left)
            right = self.check_node(node.type_right)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if left == self.token_types.STRING or right == self.token_types.STRING:
                    return self.token_types.STRING
                elif left == self.token_types.FLOAT or right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif left == self.token_types.INT and right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, TypeBinaryOperationNode) and isinstance(node.type_right, TypeValueNode):
            left = self.check_type_binary_operation_node(node.type_left)
            right = self.check_type_value_node(node.type_right)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if left == self.token_types.STRING or right == self.token_types.STRING:
                    return self.token_types.STRING
                elif left == self.token_types.FLOAT or right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif left == self.token_types.INT and right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        elif isinstance(node.type_left, TypeValueNode) and isinstance(node.type_right, TypeBinaryOperationNode):
            left = self.check_type_value_node(node.type_left)
            right = self.check_type_binary_operation_node(node.type_right)
            if node.operator in [self.token_types.NEQ, self.token_types.EQ, self.token_types.LT, self.token_types.GT, self.token_types.LTE, self.token_types.GTE]:
                return self.token_types.BOOLEAN
            elif node.operator in [self.token_types.PLUS, self.token_types.MINUS, self.token_types.MUL, self.token_types.DIV, self.token_types.MOD]:
                if left == self.token_types.STRING or right == self.token_types.STRING:
                    return self.token_types.STRING
                elif left == self.token_types.FLOAT or right == self.token_types.FLOAT:
                    return self.token_types.FLOAT
                elif left == self.token_types.INT and right == self.token_types.INT:
                    return self.token_types.INT
                else:
                    self.errors.append(f"Type mismatch in binary operation: {node}")
            else:
                self.errors.append(f"Type mismatch in binary operation: {node}")
        else:
            self.errors.append(f"Type mismatch in binary operation: {node}")

    def check_type_value_node(self, node):
        if isinstance(node.type, str):
            return node.type
        else:
            return self.check_node(node.type)

    def check_type_function_declaration_node(self, node):
        parameters_checked = all(self.check_node(child) for child in node.parameters)
        body_checked = all(self.check_node(child) for child in node.body)
        return parameters_checked and body_checked

    def check_type_method_declaration_node(self, node):
        parameters_checked = all(self.check_node(child) for child in node.parameters)
        body_checked = all(self.check_node(child) for child in node.body)
        return parameters_checked and body_checked

    def check_type_return_statement_node(self, node):
        return_value = self.check_node(node.expression)
        if return_value:
            return return_value
        else:
            return True

    def check_type_variable_declaration_node(self, node):
        if isinstance(node.initialization_type, TypeValueNode):
            if node.initialization_type:
                if node.variable_type == node.initialization_type.type:
                    return True
                else:
                    self.errors.append(f"Type mismatch in variable declaration: {node}")
                    return False
            else:
                return True
        elif isinstance(node.initialization_type, TypeClassInstantiation):
            if node.variable_type == node.initialization_type.class_name:
                return True
            else:
                self.errors.append(f"Type mismatch in variable declaration: {node}")
                return False
        elif not node.initialization_type:
            return True
        elif isinstance(node.initialization_type, TypeBinaryOperationNode):
            if self.check_node(node.initialization_type) == node.variable_type:
                return True
            else:
                self.errors.append(f"Type mismatch in variable declaration: {node}")
                return False
        else:
            if node.variable_type == node.initialization_type:
                return True
            else:
                self.errors.append(f"Type mismatch in variable declaration: {node}")
                return False

    def check_type_variable_assignment_node(self, node):
        if self.check_node(node.assignment_type) == node.variable_type:
            return True
        else:
            self.errors.append(f"Type mismatch in variable assignment: {node}")
            return False

    def check_type_function_call_node(self, node: TypeFunctionCall):
        if node.function_name in self.token_types.built_in_functions:
            return True
        else:
            check_arguments = []
            for i in range(len(node.arguments)):
                if node.arguments[i].type == list(self.symbol_table.functions[node.function_name].parameters.values())[i]:
                    check_arguments.append(True)
                else:
                    self.errors.append(f"Type mismatch in function call: {node}")
                    check_arguments.append(False)
            if all(check_arguments):
                if node.type:
                    return node.type
                else:
                    return True
            else:
                self.errors.append(f"Type mismatch in function call: {node}")
                return False

    def check_type_field_access_node(self, node):
        return node.type

    def check_type_method_call_node(self, node):
        check_arguments = []
        for arguments in node.arguments:
            if node.class_name in self.symbol_table.variables:
                class_name = self.symbol_table.variables[node.class_name]
            if arguments.node.token.type == self.token_types.IDENTIFIER:
                if arguments.type == self.symbol_table.class_declarations[class_name].methods[node.method_name].parameters[arguments.node.token.value]:
                    check_arguments.append(True)
                else:
                    self.errors.append(f"Type mismatch in method call: {node}")
                    check_arguments.append(False)
            elif arguments.type in [self.token_types.FLOAT, self.token_types.INT, self.token_types.STRING, self.token_types.BOOLEAN]:
                for parameters in self.symbol_table.class_declarations[class_name].methods[node.method_name].parameters.values():
                    if arguments.type == parameters:
                        check_arguments.append(True)
                    else:
                        self.errors.append(f"Type mismatch in method call: {node}")
                        check_arguments.append(False)
            else:
                check_arguments.append(True)
        else:
            check_arguments.append(True)
        return all(check_arguments)

    def check_type_class_constructor_node(self, node):
        return node.class_name

    def check_type_class_instantiation_node(self, node):
        check_arguments = []
        for arguments in node.arguments:
            if arguments == self.symbol_table.class_declarations[node.class_name].constructor.parameters:
                check_arguments.append(True)
            else:
                check_arguments.append(False)
        if all(check_arguments):
            print(1)
            return node.class_name
        else:
            self.errors.append(f"Type mismatch in class instantiation: {node}")
            return False

    def check_type_field_declaration_node(self, node: TypeFieldDeclaration):
        if self.check_node(node.value) == node.type:
            return True
        else:
            print(node)
            self.errors.append(f"Type mismatch in field declaration: {node}")
            return False

    def check_type_if_statement_node(self, node):
        condition_checked = self.check_node(node.condition)
        body_checked = all(self.check_node(child) for child in node.body)
        else_body_checked = all(self.check_node(child) for child in node.else_body) if node.else_body else True
        return (condition_checked == self.token_types.BOOLEAN) and body_checked and else_body_checked

    def check_type_for_statement_node(self, node):
        initializer_checked = self.check_node(node.variable)
        condition_checked = self.check_node(node.condition)
        increment_checked = self.check_node(node.increment)
        body_checked = all(self.check_node(child) for child in node.body)
        return initializer_checked and condition_checked and increment_checked and body_checked

    def check_type_while_statement_node(self, node):
        condition_checked = self.check_node(node.condition)
        body_checked = all(self.check_node(child) for child in node.body)
        return condition_checked and body_checked

    def get_errors(self):
        return self.errors
