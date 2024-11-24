import json
from .nodes import ProgramNode
from .nodes import ClassDeclaration
from .nodes import FunctionDeclaration
from .nodes import VariableDeclaration
from .nodes import VariableAssignment
from .nodes import BinaryOperationNode
from .nodes import IfStatement
from .nodes import ForStatement
from .nodes import WhileStatement
from .nodes import ValueNode
from .nodes import FieldAccess
from .nodes import MethodCall
from .nodes import ClassConstructor
from .nodes import ClassInstantiation
from .nodes import FunctionCall
from ..Tokens.token_types import TokenTypes


class Parser:
    def __init__(self, tokens):
        self.token_types = TokenTypes()
        self.tokens = tokens
        self.ast = {}

    def parse(self):
        program = ProgramNode(self.parse_program())
        self.ast = program.dictionary()
        with open("src/SemanticsAnalysis/ast.json", "w") as file:
            json.dump(self.ast, file, indent=4)
        return program

    def parse_program(self):
        body = []
        while self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type in [self.token_types.FOR, self.token_types.WHILE,
                                       self.token_types.IF, self.token_types.VAR]:
                body.append(self.parse_statement())
            elif self.tokens[0].type == self.token_types.CLASS:
                body.append(self.parse_class_declaration())
            elif self.tokens[0].type == self.token_types.FUNCTION:
                body.append(self.parse_function_declaration())
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.EOF:
            raise Exception("Expected EOF")
        return body

    def parse_class_declaration(self):
        if self.tokens[0].type != self.token_types.CLASS:
            raise Exception("Expected class declaration")
        self.tokens.pop(0)
        class_name = self.tokens.pop(0).value
        extends_class_name = None
        if self.tokens[0].type == self.token_types.LPAREN:
            self.tokens.pop(0)
            extends_class_name = self.tokens.pop(0).value
            self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected {")
        self.tokens.pop(0)
        fields = []
        methods = []
        while self.tokens[0].type != self.token_types.RBRACE:
            if self.tokens[0].type == self.token_types.VAR:
                fields.append(self.parse_variable_declaration())
            elif self.tokens[0].type == self.token_types.FUNCTION:
                methods.append(self.parse_function_declaration(is_method=True, class_name=class_name))
        self.tokens.pop(0)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return ClassDeclaration(class_name, extends_class_name, fields, methods)

    def parse_function_declaration(self, is_method=False, class_name=None):
        if self.tokens[0].type != self.token_types.FUNCTION:
            raise Exception("Expected function declaration")
        self.tokens.pop(0)
        function_name = self.tokens.pop(0).value
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected (")
        self.tokens.pop(0)
        parameters = []
        while self.tokens[0].type != self.token_types.RPAREN:
            parameters.append(self.parse_variable_declaration(is_parameter=True))
            if self.tokens[0].type == self.token_types.COMMA:
                self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected )")
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected {")
        self.tokens.pop(0)
        body = []
        while self.tokens[0].type != self.token_types.RBRACE:
            body.append(self.parse_statement())
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected }")
        self.tokens.pop(0)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        if is_method:
            if function_name == "init":
                return ClassConstructor(class_name, parameters, body)
            return FunctionDeclaration(function_name, parameters, body)
        return FunctionDeclaration(function_name, parameters, body)

    def parse_variable_declaration(self, is_parameter=False):
        if is_parameter:
            if self.tokens[0].type != self.token_types.IDENTIFIER:
                raise Exception("Expected identifier")
            variable_name = self.tokens.pop(0).value
            if self.tokens[0].type != self.token_types.COLON:
                raise Exception("Expected :")
            self.tokens.pop(0)
            variable_type = self.tokens.pop(0).value
            if self.tokens[0].type == self.token_types.ASSIGN:
                self.tokens.pop(0)
                initial_value = self.parse_expression()
                if self.tokens[0].type == self.token_types.SEMICOLON:
                    self.tokens.pop(0)
                return VariableDeclaration(variable_name, variable_type, initial_value)
            if self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            return VariableDeclaration(variable_name, variable_type)
        else:
            if self.tokens[0].type != self.token_types.VAR:
                raise Exception("Expected var")
            self.tokens.pop(0)
            variable_name = self.tokens.pop(0).value
            if self.tokens[0].type != self.token_types.COLON:
                raise Exception("Expected :")
            self.tokens.pop(0)
            variable_type = self.tokens.pop(0).value
            if self.tokens[0].type == self.token_types.ASSIGN:
                self.tokens.pop(0)
                initial_value = self.parse_expression()
                if self.tokens[0].type == self.token_types.SEMICOLON:
                    self.tokens.pop(0)
                return VariableDeclaration(variable_name, variable_type, initial_value)
            if self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            return VariableDeclaration(variable_name, variable_type)

    def parse_statement(self):
        if self.tokens[0].type == self.token_types.FOR:
            return self.parse_for_statement()
        elif self.tokens[0].type == self.token_types.WHILE:
            return self.parse_while_statement()
        elif self.tokens[0].type == self.token_types.IF:
            return self.parse_if_statement()
        elif self.tokens[0].type == self.token_types.VAR:
            return self.parse_variable_declaration()
        elif self.tokens[0].type == self.token_types.IDENTIFIER:
            return self.parse_variable_assignment()

    def parse_variable_assignment(self):
        if self.tokens[0].type != self.token_types.IDENTIFIER:
            raise Exception("Expected identifier")
        if self.tokens[1].type == self.token_types.DOT:
            return self.parse_class_field_access_and_method_call()
        variable_name = self.tokens.pop(0).value
        if self.tokens[0].type != self.token_types.ASSIGN:
            raise Exception("Expected =")
        self.tokens.pop(0)
        expression = self.parse_expression()
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return VariableAssignment(variable_name, expression)

    def parse_for_statement(self):
        if self.tokens[0].type != self.token_types.FOR:
            raise Exception("Expected for")
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected (")
        self.tokens.pop(0)
        initialization = self.parse_variable_declaration()
        if self.tokens[0].type != self.token_types.SEMICOLON:
            raise Exception("Expected ;")
        self.tokens.pop(0)
        condition = self.parse_expression()
        if self.tokens[0].type != self.token_types.SEMICOLON:
            raise Exception("Expected ;")
        self.tokens.pop(0)
        increment = self.parse_variable_assignment()
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected )")
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected {")
        self.tokens.pop(0)
        body = self.parse_statement()
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected }")
        self.tokens.pop(0)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return ForStatement(initialization, condition, increment, body)

    def parse_while_statement(self):
        if self.tokens[0].type != self.token_types.WHILE:
            raise Exception("Expected while")
        self.tokens.pop(0)
        condition = self.parse_expression()
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected {")
        self.tokens.pop(0)
        body = self.parse_statement()
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected }")
        self.tokens.pop(0)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return WhileStatement(condition, body)

    def parse_if_statement(self):
        self.tokens.pop(0)
        condition = self.parse_expression()
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected {")
        self.tokens.pop(0)
        body = []
        while self.tokens[0].type != self.token_types.RBRACE:
            body.append(self.parse_statement())
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected }")
        self.tokens.pop(0)
        else_body = None
        if self.tokens[0].type == self.token_types.ELSE:
            self.tokens.pop(0)
            if self.tokens[0].type != self.token_types.LBRACE:
                raise Exception("Expected {")
            self.tokens.pop(0)
            else_body = []
            while self.tokens[0].type != self.token_types.RBRACE:
                else_body.append(self.parse_statement())
            if self.tokens[0].type != self.token_types.RBRACE:
                raise Exception("Expected }")
            self.tokens.pop(0)
            if self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return IfStatement(condition, body, else_body)

    def parse_expression(self):
        if self.tokens[1].type == self.token_types.DOT:
            return self.parse_class_field_access_and_method_call()
        return self.parse_equalities()

    def parse_class_field_access_and_method_call(self):
        node = self.parse_primary()
        while self.tokens[0].type == self.token_types.DOT:
            self.tokens.pop(0)
            if self.tokens[0].type != self.token_types.IDENTIFIER:
                raise Exception("Expected identifier")
            field_name = self.parse_primary()
            if self.tokens[0].type == self.token_types.LPAREN:
                self.tokens.pop(0)
                arguments = []
                while self.tokens[0].type != self.token_types.RPAREN:
                    arguments.append(self.parse_expression())
                    if self.tokens[0].type == self.token_types.COMMA:
                        self.tokens.pop(0)
                if self.tokens[0].type != self.token_types.RPAREN:
                    raise Exception("Expected )")
                self.tokens.pop(0)
                node = MethodCall(node, field_name, arguments)
            else:
                node = FieldAccess(node, field_name)
        return node

    def parse_equalities(self):
        node = self.parse_addition_subtraction()
        while self.tokens[0].type in [self.token_types.EQ, self.token_types.NEQ, self.token_types.GT,
                                      self.token_types.GTE, self.token_types.LT, self.token_types.LTE,
                                      self.token_types.AND, self.token_types.OR]:
            operator = self.tokens.pop(0).type
            right = self.parse_addition_subtraction()
            node = BinaryOperationNode(node, operator, right)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return node

    def parse_addition_subtraction(self):
        node = self.parse_multiplication_division()
        while self.tokens[0].type in [self.token_types.PLUS, self.token_types.MINUS]:
            operator = self.tokens.pop(0).type
            right = self.parse_multiplication_division()
            node = BinaryOperationNode(node, operator, right)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return node

    def parse_multiplication_division(self):
        node = self.parse_primary()
        while self.tokens[0].type in [self.token_types.MUL, self.token_types.DIV]:
            operator = self.tokens.pop(0).type
            right = self.parse_primary()
            node = BinaryOperationNode(node, operator, right)
        if self.tokens[0].type == self.token_types.SEMICOLON:
            self.tokens.pop(0)
        return node

    def parse_primary(self):
        if self.tokens[0].type in [self.token_types.INT, self.token_types.FLOAT,
                                   self.token_types.BOOLEAN, self.token_types.STRING]:
            return ValueNode(self.tokens.pop(0))
        elif self.tokens[0].type == self.token_types.IDENTIFIER:
            return self.tokens.pop(0)
        elif self.tokens[0].type == self.token_types.LPAREN:
            self.tokens.pop(0)
            node = self.parse_expression()
            if self.tokens[0].type != self.token_types.RPAREN:
                print(self.tokens[0].type)
                raise Exception("Expected )")
            self.tokens.pop(0)
            return node
        elif self.tokens[0].type == self.token_types.NEW:
            self.tokens.pop(0)
            if self.tokens[0].type != self.token_types.IDENTIFIER:
                raise Exception("Expected identifier")
            class_name = self.tokens.pop(0).value
            if self.tokens[0].type != self.token_types.LPAREN:
                raise Exception("Expected (")
            self.tokens.pop(0)
            arguments = []
            while self.tokens[0].type != self.token_types.RPAREN:
                arguments.append(self.parse_expression())
                if self.tokens[0].type == self.token_types.COMMA:
                    self.tokens.pop(0)
            if self.tokens[0].type != self.token_types.RPAREN:
                raise Exception("Expected )")
            self.tokens.pop(0)
            return ClassInstantiation(class_name, arguments)
        elif self.tokens[0].type == self.token_types.IDENTIFIER and self.tokens[1].type == self.token_types.LPAREN:
            function_name = self.tokens.pop(0).value
            self.tokens.pop(0)
            arguments = []
            while self.tokens[0].type != self.token_types.RPAREN:
                arguments.append(self.parse_expression())
                if self.tokens[0].type == self.token_types.COMMA:
                    self.tokens.pop(0)
            if self.tokens[0].type != self.token_types.RPAREN:
                raise Exception("Expected )")
            self.tokens.pop(0)
            return FunctionCall(function_name, arguments)
        print(self.tokens[0])
        raise Exception("Expected number, identifier, or (")
