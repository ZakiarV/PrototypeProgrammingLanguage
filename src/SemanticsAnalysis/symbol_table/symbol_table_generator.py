import json
from src.Tokens.token_types import TokenTypes
from .symbol_table import ProgramSymbolTable, FunctionSymbolTable, ClassSymbolTable
from src.SyntaxAnalysis.nodes import (ProgramNode, ClassDeclaration, VariableDeclaration, FunctionDeclaration,
                                      ReturnStatement, ValueNode, BinaryOperationNode, ClassInstantiation, ForStatement,
                                      FunctionCall)


class SymbolTableGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = ProgramSymbolTable()
        self.token_types = TokenTypes()

    def generate(self):
        self.visit(self.ast, self.symbol_table)
        with open('src/SemanticsAnalysis/symbol_table/symbol_table.json', 'w') as f:
            dictionary = self.symbol_table.dictionary()
            json.dump(dictionary, f, indent=4)
        return self.symbol_table

    def visit(self, node, symbol_table):
        if isinstance(node, ProgramNode):
            self.visit_program(node, symbol_table)

    def visit_program(self, node, symbol_table):
        for body in node.body_ast:
            if isinstance(body, ClassDeclaration):
                self.visit_class_declaration(body, symbol_table)
            elif isinstance(body, VariableDeclaration):
                self.visit_variable_declaration(body, symbol_table)
            elif isinstance(body, FunctionDeclaration):
                self.visit_function_declaration(body, symbol_table)
            elif isinstance(body, ForStatement):
                self.visit_for_statement(body, symbol_table)
            elif isinstance(body, FunctionCall):
                self.visit_function_call(body, symbol_table)

    def visit_class_declaration(self, node, symbol_table):
        symbol_table.add_class_declaration(node.class_name)
        class_symbol_table = symbol_table.class_declarations[node.class_name]
        if node.extends_class_name:
            class_symbol_table.set_extends(node.extends_class_name)
        if node.constructor:
            self.visit_constructor_declaration(node.constructor, class_symbol_table)
        for field in node.fields:
            self.visit_field_declaration(field, class_symbol_table)
        for method in node.methods:
            self.visit_method_declaration(method, class_symbol_table)

    def visit_field_declaration(self, node, class_symbol_table):
        if isinstance(node.initial_value, ClassInstantiation):
            class_symbol_table.add_field(node.variable_name, node.initial_value.class_name)
        else:
            class_symbol_table.add_field(node.variable_name, node.variable_type)

    def visit_method_declaration(self, node, class_symbol_table):
        class_symbol_table.add_method(node.function_name)
        method_symbol_table = class_symbol_table.methods[node.function_name]
        for param in node.parameters:
            method_symbol_table.add_parameter(param.variable_name, param.variable_type)
        for statement in node.body_ast:
            if isinstance(statement, VariableDeclaration):
                self.visit_variable_declaration(statement, method_symbol_table)
            elif isinstance(statement, ReturnStatement):
                self.visit_return_statement(statement, method_symbol_table)
            elif isinstance(statement, ForStatement):
                self.visit_for_statement(statement, method_symbol_table)
            elif isinstance(statement, FunctionCall):
                self.visit_function_call(statement, method_symbol_table)

    def visit_return_statement(self, node, symbol_table: FunctionSymbolTable):
        if isinstance(node.expression, ValueNode):
            if node.expression.token.type == self.token_types.IDENTIFIER:
                type_ = symbol_table.variables[node.expression.token.value]
                symbol_table.set_return_type(type_)
            else:
                symbol_table.set_return_type(node.expression.token.type)
        elif isinstance(node.expression, BinaryOperationNode):
            type_ = self.visit_binary_operation(node.expression, symbol_table)
            symbol_table.set_return_type(type_)
        elif isinstance(node.expression, FunctionCall):
            symbol_table.set_return_type(node.expression.function_name)

    def visit_constructor_declaration(self, node, class_symbol_table):
        class_symbol_table.set_constructors()
        constructor_symbol_table = class_symbol_table.constructor
        for statement in node.body_ast:
            if isinstance(statement, VariableDeclaration):
                self.visit_field_declaration(statement, class_symbol_table)
            elif isinstance(statement, ForStatement):
                self.visit_for_statement(statement, constructor_symbol_table)
        for param in node.parameters:
            constructor_symbol_table.add_parameter(param.variable_name, param.variable_type)
        constructor_symbol_table.set_return_type(class_symbol_table.name)

    def visit_function_declaration(self, node, symbol_table):
        symbol_table.add_function(node.function_name)
        function_symbol_table = symbol_table.functions[node.function_name]
        for param in node.parameters:
            function_symbol_table.add_parameter(param.variable_name, param.variable_type)
        for statement in node.body_ast:
            if isinstance(statement, VariableDeclaration):
                self.visit_variable_declaration(statement, function_symbol_table)
            elif isinstance(statement, ReturnStatement):
                self.visit_return_statement(statement, function_symbol_table)
            elif isinstance(statement, ForStatement):
                self.visit_for_statement(statement, function_symbol_table)
            elif isinstance(statement, FunctionCall):
                self.visit_function_call(statement, function_symbol_table)

    def visit_variable_declaration(self, node, symbol_table):
        if node.variable_type:
            if isinstance(node.initial_value, ClassInstantiation):
                symbol_table.add_variable(node.variable_name, node.initial_value.class_name)
            elif isinstance(node.initial_value, ValueNode):
                symbol_table.add_variable(node.variable_name, node.variable_type)
            elif isinstance(node.initial_value, FunctionCall):
                symbol_table.add_variable(node.variable_name, node.initial_value.function_name)
                self.visit(node.initial_value, symbol_table)
        elif isinstance(node.initial_value, BinaryOperationNode):
            type_ = self.visit_binary_operation(node.initial_value, symbol_table)
            symbol_table.add_variable(node.variable_name, type_)
        else:
            node_type = node.initial_value.token.type
            symbol_table.add_variable(node.variable_name, node_type)

    def visit_binary_operation(self, node, symbol_table):
        if node.operator in [">=", "<=", ">", "<", "==", "!="]:
            return self.token_types.BOOLEAN
        left = node.left
        right = node.right
        left_type = None
        if isinstance(left, BinaryOperationNode):
            left_type = self.visit_binary_operation(left, symbol_table)
        elif isinstance(left, ValueNode):
            if left.token.type == self.token_types.IDENTIFIER:
                if isinstance(symbol_table, FunctionSymbolTable):
                    if left.token.value in symbol_table.parameters.keys():
                        left_type = symbol_table.parameters[left.token.value]
                    else:
                        left_type = symbol_table.variables[left.token.value]
                elif isinstance(symbol_table, ProgramSymbolTable):
                    left_type = symbol_table.get_variable(left.token.value)
                elif isinstance(symbol_table, ClassSymbolTable):
                    left_type = symbol_table.get_field(left.token.value)
            else:
                left_type = left.token.type

        right_type = None
        if isinstance(right, BinaryOperationNode):
            right_type = self.visit_binary_operation(right, symbol_table)
        elif isinstance(right, ValueNode):
            if right.token.type == self.token_types.IDENTIFIER:
                if isinstance(symbol_table, FunctionSymbolTable):
                    if right.token.value in symbol_table.parameters.keys():
                        right_type = symbol_table.parameters[right.token.value]
                    else:
                        right_type = symbol_table.variables[right.token.value]
                elif isinstance(symbol_table, ProgramSymbolTable):
                    right_type = symbol_table.get_variable(right.token.value)
                elif isinstance(symbol_table, ClassSymbolTable):
                    right_type = symbol_table.get_field(right.token.value)
            else:
                right_type = right.token.type

        if left_type == self.token_types.FLOAT or right_type == self.token_types.FLOAT:
            return self.token_types.FLOAT
        elif left_type == self.token_types.INT and right_type == self.token_types.INT:
            return self.token_types.INT
        elif left_type == self.token_types.STRING and right_type == self.token_types.STRING:
            return self.token_types.STRING
        elif left_type == self.token_types.BOOLEAN and right_type == self.token_types.BOOLEAN:
            return self.token_types.BOOLEAN
        else:
            raise TypeError(f"Invalid binary operation between types {left_type} and {right_type}")

    def visit_for_statement(self, node, symbol_table):
        if node.initializer.variable_type:
            symbol_table.add_for_loop_var(node.initializer.variable_name, node.initializer.variable_type)
        else:
            symbol_table.add_for_loop_var(node.initializer.variable_name, node.initializer.initial_value.token.type)

    def visit_function_call(self, node, symbol_table):
        if node.is_builtin:
            self.symbol_table.add_built_in_function(node.function_name, node.function_name)
