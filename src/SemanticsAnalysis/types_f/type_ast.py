import json

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
from src.SyntaxAnalysis.nodes import FunctionDeclaration
from src.SyntaxAnalysis.nodes import VariableDeclaration
from src.SyntaxAnalysis.nodes import VariableAssignment
from src.SyntaxAnalysis.nodes import BinaryOperationNode
from src.SyntaxAnalysis.nodes import IfStatement
from src.SyntaxAnalysis.nodes import ForStatement
from src.SyntaxAnalysis.nodes import WhileStatement
from src.SyntaxAnalysis.nodes import ValueNode
from src.SyntaxAnalysis.nodes import FieldAccess
from src.SyntaxAnalysis.nodes import MethodCall
from src.SyntaxAnalysis.nodes import ClassConstructor
from src.SyntaxAnalysis.nodes import ClassInstantiation
from src.SyntaxAnalysis.nodes import FunctionCall
from src.SyntaxAnalysis.nodes import ReturnStatement

from src.SemanticsAnalysis.symbol_table.symbol_table import ProgramSymbolTable
from src.SemanticsAnalysis.symbol_table.symbol_table import ClassSymbolTable
from src.SemanticsAnalysis.symbol_table.symbol_table import FunctionSymbolTable
from src.SemanticsAnalysis.symbol_table.symbol_table import ForSymbolTable

from src.Tokens.token_types import TokenTypes


class TypeAST:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
        self.token_types = TokenTypes()

    def analyze(self):
        ast = self.visit(self.ast, self.symbol_table)
        with open("src/SemanticsAnalysis/types_f/type_ast.json", "w") as file:
            json.dump(ast.dictionary(), file, indent=4)
        return ast

    def visit(self, node, symbol_table):
        if isinstance(node, ProgramNode):
            return self.visit_program(node, symbol_table)
        elif isinstance(node, ClassDeclaration):
            return self.visit_class_declaration(node, symbol_table)
        elif isinstance(node, FunctionDeclaration):
            return self.visit_function_declaration(node, symbol_table)
        elif isinstance(node, VariableDeclaration):
            return self.visit_variable_declaration(node, symbol_table)
        elif isinstance(node, VariableAssignment):
            return self.visit_variable_assignment(node, symbol_table)
        elif isinstance(node, BinaryOperationNode):
            return self.visit_binary_operation(node, symbol_table)
        elif isinstance(node, IfStatement):
            return self.visit_if_statement(node, symbol_table)
        elif isinstance(node, ForStatement):
            return self.visit_for_statement(node, symbol_table)
        elif isinstance(node, WhileStatement):
            return self.visit_while_statement(node, symbol_table)
        elif isinstance(node, ValueNode):
            return self.visit_value_node(node, symbol_table)
        elif isinstance(node, FieldAccess):
            return self.visit_field_access(node, symbol_table)
        elif isinstance(node, MethodCall):
            return self.visit_method_call(node, symbol_table)
        elif isinstance(node, ClassConstructor):
            return self.visit_class_constructor(node, symbol_table)
        elif isinstance(node, ClassInstantiation):
            return self.visit_class_instantiation(node, symbol_table)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node, symbol_table)
        elif isinstance(node, ReturnStatement):
            return self.visit_return_statement(node, symbol_table)
        else:
            raise Exception(f"Unknown node type {type(node)}, {node}")

    def visit_program(self, node, symbol_table):
        body_ast = []
        for statement in node.body_ast:
            body_ast.append(self.visit(statement, symbol_table))
        return ProgramNode(body_ast)

    def visit_binary_operation(self, node, symbol_table):
        left = self.visit(node.left, symbol_table)
        right = self.visit(node.right, symbol_table)
        return TypeBinaryOperationNode(left, node.operator, right, node)

    def visit_value_node(self, node, symbol_table):
        if node.token.type == self.token_types.IDENTIFIER:
            if isinstance(symbol_table, ProgramSymbolTable):
                variable = symbol_table.get_variable(node.token.value)
                if variable:
                    return TypeValueNode(variable, node)
                else:
                    variable = symbol_table.get_for_loop_var(node.token.value)
                    if variable:
                        return TypeValueNode(variable.loop_variable_type, node)
                    else:
                        raise Exception(f"Declaration {node.token.value} not found")
            elif isinstance(symbol_table, ClassSymbolTable):
                field = symbol_table.get_field(node.token.value)
                if field:
                    return TypeValueNode(field, node)
                else:
                    if symbol_table.constructor.parameters[node.token.value]:
                        return TypeValueNode(symbol_table.constructor.parameters[node.token.value], node)
            elif isinstance(symbol_table, FunctionSymbolTable):
                variable = symbol_table.get_variable(node.token.value)
                if variable:
                    return TypeValueNode(variable, node)
                elif isinstance(symbol_table.parent, ProgramSymbolTable):
                    variable = symbol_table.parent.get_variable(node.token.value)
                    if variable:
                        return TypeValueNode(variable, node)
                    elif symbol_table.parent.get_variable(node.token.value):
                        return TypeValueNode(symbol_table.parent.get_variable(node.token.value), node)
                    elif symbol_table.parameters[node.token.value]:
                        return TypeValueNode(symbol_table.parameters[node.token.value], node)
                elif symbol_table.function_name == "init":
                    try:
                        variable = symbol_table.parameters[node.token.value]
                    except KeyError:
                        variable = symbol_table.parent.fields[node.token.value]
                    if variable:
                        return TypeValueNode(variable, node)
                    else:
                        raise Exception(f"Declaration {node.token.value} not found")
                elif isinstance(symbol_table.parent, ClassSymbolTable):
                    variable = symbol_table.get_variable(node.token.value)
                    if variable:
                        return TypeValueNode(variable, node)
                    elif symbol_table.parent.get_field(node.token.value):
                        return TypeValueNode(symbol_table.parent.get_field(node.token.value), node)
                    elif symbol_table.parent.get_method(node.token.value):
                        return TypeValueNode(symbol_table.parent.get_method(node.token.value), node)
                    elif symbol_table.parent.get_field(node.token.value):
                        return TypeValueNode(symbol_table.parent.get_field(node.token.value), node)
                    elif symbol_table.parameters[node.token.value]:
                        return TypeValueNode(symbol_table.parameters[node.token.value], node)
            elif isinstance(symbol_table, ForSymbolTable):
                variable = symbol_table.loop_variable_type
                if variable:
                    return TypeValueNode(variable, node)
                else:
                    raise Exception(f"Declaration {node.token.value} not found")
            else:
                raise Exception(f"Declaration {node.token.value} not found")
        else:
            return TypeValueNode(node.token.type, node)

    def visit_class_declaration(self, node, symbol_table):
        class_symbol_table = symbol_table.class_declarations[node.class_name]
        fields = []
        for field in node.fields:
            fields.append(self.visit(field, class_symbol_table))
        methods = []
        for method in node.methods:
            methods.append(self.visit(method, class_symbol_table))
        constructor = self.visit(node.constructor, class_symbol_table) if node.constructor else None
        return ClassDeclaration(node.class_name, node.extends_class_name, fields, methods, constructor)

    def visit_function_declaration(self, node, symbol_table):
        if isinstance(symbol_table, ProgramSymbolTable):
            function_symbol_table = symbol_table.functions[node.function_name]
        elif isinstance(symbol_table, ClassSymbolTable):
            function_symbol_table = symbol_table.methods[node.function_name]
        else:
            raise Exception("Function declaration not found")
        parameters = []
        for parameter in node.parameters:
            parameters.append(self.visit(parameter, function_symbol_table))
        body = []
        for statement in node.body_ast:
            body.append(self.visit(statement, function_symbol_table))
        for statement in body:
            if isinstance(statement, TypeReturnStatement):
                return_type = statement.type
                break
        else:
            return_type = None
        if isinstance(symbol_table, ProgramSymbolTable):
            return TypeFunctionDeclaration(return_type, node.function_name, parameters, body, node)
        elif isinstance(symbol_table, ClassSymbolTable):
            return TypeMethodDeclaration(return_type, symbol_table.name, node.function_name, parameters, body, node)
        else:
            raise Exception("Function declaration not found")

    def visit_variable_declaration(self, node, symbol_table):
        if node.is_parameter:
            type_ = symbol_table.parameters[node.variable_name]
            return TypeVariableDeclaration(node.variable_name, type_ if not node.variable_type else node.variable_type,
                                           None, node)
        elif node.class_name and node.function_name:
            if node.function_name == "init":
                type_ = symbol_table.parent.fields[node.variable_name]
                if not type_:
                    type_ = symbol_table.constructor.parameters[node.variable_name]
            else:
                type_ = symbol_table.variables[node.variable_name]
            initial_type = self.visit(node.initial_value, symbol_table)
            return TypeVariableDeclaration(node.variable_name, node.variable_type if not type_ else type_,
                                           initial_type, node)
        elif node.class_name:
            initial_type = self.visit(node.initial_value, symbol_table)
            type_ = symbol_table.fields[node.variable_name]
            return TypeFieldDeclaration(node.class_name, node.variable_name,
                                        node.variable_type if not type_ else type_, initial_type, node)
        elif node.function_name:
            initial_type = self.visit(node.initial_value, symbol_table)
            type_ = symbol_table.variables[node.variable_name]
            return TypeVariableDeclaration(node.variable_name, node.variable_type if not type_ else type_,
                                           initial_type, node)
        elif isinstance(symbol_table, ForSymbolTable):
            type_ = symbol_table.loop_variable_type
            initial_type = self.visit(node.initial_value, symbol_table) if node.initial_value else None
            return TypeVariableDeclaration(node.variable_name, node.variable_type if not type_ else type_,
                                           initial_type, node)
        else:
            initial_type = self.visit(node.initial_value, symbol_table) if node.initial_value else None
            type_ = symbol_table.get_variable(node.variable_name)
            return TypeVariableDeclaration(node.variable_name, node.variable_type if not type_ else type_,
                                           type_ if not initial_type else initial_type, node)

    def visit_variable_assignment(self, node, symbol_table):
        if isinstance(symbol_table, ProgramSymbolTable):
            type_ = symbol_table.get_variable(node.variable_name)
        elif isinstance(symbol_table, ClassSymbolTable):
            type_ = symbol_table.get_field(node.variable_name)
        elif isinstance(symbol_table, FunctionSymbolTable):
            type_ = symbol_table.get_variable(node.variable_name)
        elif isinstance(symbol_table, ForSymbolTable):
            type_ = symbol_table.loop_variable_type
        else:
            raise Exception("Variable declaration not found")
        assignment_type = self.visit(node.expression, symbol_table)
        return TypeVariableAssignment(node.variable_name, type_, assignment_type, node)

    def visit_if_statement(self, node, symbol_table):
        condition = self.visit(node.condition, symbol_table)
        body = []
        for statement in node.body_ast:
            body.append(self.visit(statement, symbol_table))
        else_body = []
        if node.else_body_ast:
            else_body = []
            for statement in node.else_body_ast:
                else_body.append(self.visit(statement, symbol_table))
        return TypeIfStatement(condition, body, else_body, node)

    def visit_for_statement(self, node, symbol_table):
        for_loop_symbol_table = symbol_table.get_for_loop_var(node.initializer.variable_name)
        variable_declaration = self.visit(node.initializer, for_loop_symbol_table)
        condition = self.visit(node.condition, for_loop_symbol_table)
        increment = self.visit(node.increment, for_loop_symbol_table)
        body = []
        for statement in node.body_ast:
            body.append(self.visit(statement, symbol_table))
        return TypeForStatement(variable_declaration, condition, increment, body, node)

    def visit_while_statement(self, node, symbol_table):
        condition = self.visit(node.condition, symbol_table)
        body = []
        for statement in node.body_ast:
            body.append(self.visit(statement, symbol_table))
        return TypeWhileStatement(condition, body, node)

    def visit_field_access(self, node, symbol_table):
        if isinstance(symbol_table, ProgramSymbolTable):
            field = symbol_table.class_declarations[node.instance].fields[node.field_name]
        elif isinstance(symbol_table, ClassSymbolTable):
            if node.instance == symbol_table.name:
                field = symbol_table.fields[node.field_name]
            else:
                field = symbol_table.parent.class_declarations[node.instance].fields[node.field_name]
        elif isinstance(symbol_table, FunctionSymbolTable):
            if isinstance(symbol_table.parent, ClassSymbolTable):
                field = symbol_table.parent.parent.class_declarations[node.instance].fields[node.field_name]
            else:
                field = symbol_table.parent.class_declarations[node.instance].fields[node.field_name]
        else:
            raise Exception("Field declaration not found")

        return TypeFieldAccess(node.instance, node.field_name, field, node)

    def visit_method_call(self, node, symbol_table):
        if isinstance(symbol_table, ProgramSymbolTable):
            class_name = symbol_table.variables[node.instance]
            field = symbol_table.class_declarations[class_name].methods[node.method_name]
        elif isinstance(symbol_table, ClassSymbolTable):
            if node.instance == symbol_table.name:
                field = symbol_table.methods[node.method_name]
            else:
                field = symbol_table.parent.class_declarations[node.instance].methods[node.method_name]
        elif isinstance(symbol_table, FunctionSymbolTable):
            if isinstance(symbol_table.parent, ClassSymbolTable):
                if node.method_name == "init":
                    class_name = symbol_table.parent.fields[node.instance]
                else:
                    try:
                        class_name = symbol_table.parent.fields[node.instance]
                    except KeyError:
                        class_name = symbol_table.variables[node.instance]
                field = symbol_table.parent.parent.class_declarations[class_name].methods[node.method_name]
            else:
                field = symbol_table.parent.class_declarations[node.instance].methods[node.method_name]
        else:
            raise Exception("Field declaration not found")

        arguments = []
        for argument in node.arguments:
            arguments.append(self.visit(argument, symbol_table))

        return TypeMethodCall(node.instance, node.method_name, arguments, field.return_type, node)

    def visit_class_constructor(self, node, symbol_table):
        function_symbol_table = symbol_table.constructor
        parameters = []
        for parameter in node.parameters:
            parameters.append(self.visit(parameter, function_symbol_table))
        body = []
        for statement in node.body_ast:
            body.append(self.visit(statement, function_symbol_table))
        body.append(TypeReturnStatement(symbol_table.name, None, node))
        return TypeClassConstructor(node.class_name, parameters, body, node)

    def visit_class_instantiation(self, node, symbol_table):
        arguments = []
        for argument in node.arguments:
            arguments.append(self.visit(argument, symbol_table))
        return TypeClassInstantiation(node.class_name, arguments, node)

    def visit_function_call(self, node, symbol_table):
        if isinstance(symbol_table, ProgramSymbolTable):
            if node.function_name in symbol_table.built_in_functions:
                function_symbol_table = symbol_table.built_in_functions[node.function_name]
            else:
                function_symbol_table = symbol_table.functions[node.function_name]
        elif isinstance(symbol_table, ClassSymbolTable):
            if node.function_name in symbol_table.parent.built_in_functions:
                function_symbol_table = symbol_table.parent.built_in_functions[node.function_name]
            else:
                function_symbol_table = symbol_table.parent.functions[node.function_name]
        elif isinstance(symbol_table, FunctionSymbolTable):
            if isinstance(symbol_table.parent, ClassSymbolTable):
                if node.function_name in symbol_table.parent.parent.built_in_functions:
                    function_symbol_table = symbol_table.parent.parent.built_in_functions[node.function_name]
                else:
                    function_symbol_table = symbol_table.parent.parent.functions[node.function_name]
            else:
                if node.function_name in symbol_table.parent.built_in_functions:
                    function_symbol_table = symbol_table.parent.built_in_functions[node.function_name]
                else:
                    function_symbol_table = symbol_table.parent.functions[node.function_name]
        else:
            raise Exception("Function declaration not found")
        arguments = []
        for argument in node.arguments:
            arguments.append(self.visit(argument, symbol_table))
        if isinstance(function_symbol_table, FunctionSymbolTable):
            return_type = function_symbol_table.return_type
        elif isinstance(function_symbol_table, str):
            return_type = function_symbol_table
        else:
            raise Exception("Function declaration not found")
        return TypeFunctionCall(node.function_name, arguments, return_type, node)

    def visit_return_statement(self, node, symbol_table):
        if isinstance(symbol_table, FunctionSymbolTable) and symbol_table.function_name == "init":
            return TypeReturnStatement(symbol_table.parent.name, None, node)
        elif isinstance(symbol_table, FunctionSymbolTable) and isinstance(symbol_table.parent, ClassSymbolTable):
            return TypeReturnStatement(symbol_table.return_type, self.visit(node.expression, symbol_table), node)
        else:
            return TypeReturnStatement(symbol_table.return_type, self.visit(node.expression, symbol_table), node)
