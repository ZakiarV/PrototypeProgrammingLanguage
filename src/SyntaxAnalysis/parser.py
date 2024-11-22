from .nodes import ProgramNode
from .nodes import ClassDeclaration
from .nodes import FunctionDeclaration
from ..Tokens.token_types import TokenTypes


class Parser:
    def __init__(self, tokens):
        self.token_types = TokenTypes()
        self.tokens = tokens

    def parse(self):
        return ProgramNode(self.parse_program())

    def parse_program(self):
        body = []
        while self.tokens[0].type == self.token_types.EOF:
            if self.tokens[0].type == self.token_types.CLASS:
                body.append(self.parse_class_declaration())
            elif self.tokens[0].type == self.token_types.FUNCTION:
                pass
            elif self.tokens[0].type == self.token_types.VAR:
                pass
            elif self.tokens[0].type in [self.token_types.IF, self.token_types.FOR,
                                         self.token_types.WHILE]:
                body.append(self.parse_statements())
        return body

    def parse_class_declaration(self):
        self.tokens.pop(0)
        class_name = self.tokens.pop(0).value
        extends_class_name = None
        if self.tokens[0].type == self.token_types.LPAREN:
            self.tokens.pop(0)
            if self.tokens[0].type == self.token_types.IDENTIFIER:
                extends_class_name = self.tokens.pop(0).value
            self.tokens.pop(0)  # Pop ")"
        self.tokens.pop(0)  # Pop "{"
        body = self.parse_class_fields_methods()
        self.tokens.pop(0)  # Pop "}"
        return ClassDeclaration(class_name, extends_class_name, body[0], body[1])

    def parse_class_fields_methods(self):
        fields = []
        methods = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type == self.token_types.FUNCTION:
                methods.append(self.parse_function_declaration())
            elif self.tokens[0].type == self.token_types.VAR:
                fields.append(self.parse_variable_declaration())
            else:
                raise SyntaxError("Invalid token in class declaration")
        return fields, methods

    def parse_function_declaration(self):
        self.tokens.pop(0) # pop FUNCTION token
        function_name = self.tokens.pop(0).value
        self.tokens.pop(0) # pop "("
        parameters = []
        while self.tokens[0].type != self.token_types.RPAREN and self.tokens[0].type != self.token_types.EOF:
            parameters.append(self.tokens.pop(0).value)
            if self.tokens[0].type == self.token_types.COMMA:
                self.tokens.pop(0)

        self.tokens.pop(0) # pop ")"
        self.tokens.pop(0) # pop "{"
        body = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type!= self.token_types.EOF:
            body.append(self.parse_statements())
        self.tokens.pop(0) # pop "}"
        return FunctionDeclaration(function_name, parameters, body)

    def parse_variable_declaration(self):
        pass

    def parse_variable_assignment(self):
        pass

    def parse_statements(self):
        if self.tokens[0].type == self.token_types.IF:
            pass
        elif self.tokens[0].type == self.token_types.FOR:
            pass
        elif self.tokens[0].type == self.token_types.WHILE:
            pass
        elif self.tokens[0].type == self.token_types.RETURN:
            pass
        elif self.tokens[0].type == self.token_types.IDENTIFIER:
            pass

    def parse_expression(self):
        pass


