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
from .nodes import ReturnStatement

from ..Tokens.token_types import TokenTypes


class Parser:
    def __init__(self, tokens):
        self.token_types = TokenTypes()
        self.tokens = tokens
        self.ast = None

    def parse(self):
        program = ProgramNode(self.parse_program())
        self.ast = program.dictionary()
        with open("src/SemanticsAnalysis/ast.json", "w") as file:
            json.dump(self.ast, file, indent=4)
        return program

    def parse_program(self):
        body = []
        while self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type == self.token_types.CLASS:
                body.append(self.parse_class_declaration())
            elif self.tokens[0].type == self.token_types.FUNCTION:
                body.append(self.parse_function_declaration())
            elif self.tokens[0].type in [self.token_types.VAR, self.token_types.IF, self.token_types.WHILE, self.token_types.FOR, self.token_types.IDENTIFIER]:
                body.append(self.parse_statement())
            elif self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            else:
                raise Exception("Unexpected token " + str(self.tokens[0].value) + " in program.")
        return body

    def parse_class_declaration(self):
        self.tokens.pop(0) # remove class token
        class_name = self.tokens.pop(0).value # get class name
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected { after class name in class declaration " + str(class_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0) # remove {
        constructor = None
        fields = []
        methods = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type == self.token_types.FUNCTION and self.tokens[1].value == "init":
                constructor = self.parse_function_declaration(is_constructor=True, class_name=class_name)
            elif self.tokens[0].type == self.token_types.FUNCTION:
                methods.append(self.parse_function_declaration())
            elif self.tokens[0].type == self.token_types.VAR:
                fields.append(self.parse_variable_declaration())
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected } at the end of class declaration " + str(class_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0) # remove }
        return ClassDeclaration(class_name, None, fields, methods, constructor)

    def parse_function_declaration(self, is_constructor=False, class_name=None):
        self.tokens.pop(0)
        function_name = self.tokens.pop(0).value
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after function name in function declaration " + str(function_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        parameters = []
        while self.tokens[0].type != self.token_types.RPAREN and self.tokens[0].type != self.token_types.EOF:
            parameters.append(self.parse_variable_declaration(is_parameter=True))
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after function parameters in function declaration " + str(function_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0) # remove )
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected { after function declaration " + str(function_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0) # remove {
        body = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type in [self.token_types.VAR, self.token_types.IF, self.token_types.WHILE, self.token_types.FOR, self.token_types.RETURN, self.token_types.IDENTIFIER]:
                body.append(self.parse_statement())
            elif self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            else:
                raise Exception("Unexpected token " + str(self.tokens[0].value) + " in function " + function_name + " body.")
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected } at the end of function declaration " + str(function_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0) # remove }
        if is_constructor:
            return ClassConstructor(class_name, parameters, body)
        return FunctionDeclaration(function_name, parameters, body)

    def parse_statement(self):
        if self.tokens[0].type == self.token_types.VAR:
            return self.parse_variable_declaration()
        elif self.tokens[0].type == self.token_types.IF:
            return self.parse_if_statement()
        elif self.tokens[0].type == self.token_types.WHILE:
            return self.parse_while_statement()
        elif self.tokens[0].type == self.token_types.FOR:
            return self.parse_for_statement()
        elif self.tokens[0].type == self.token_types.IDENTIFIER:
            return self.parse_identifier()
        elif self.tokens[0].type == self.token_types.RETURN:
            return self.parse_return_statement()
        elif self.tokens[1].type == self.token_types.DOT and self.tokens[2].type == self.token_types.IDENTIFIER:
            return self.parse_field_method_access()
        else:
            raise Exception("Unexpected token " + str(self.tokens[0].value) + " in statement.")

    def parse_variable_declaration(self, is_parameter=False):
        if not is_parameter:
            self.tokens.pop(0)
        variable_name = self.tokens.pop(0).value
        if is_parameter:
            if self.tokens[0].type != self.token_types.COLON:
                raise Exception("Expected : after parameter name in function declaration but got " + str(self.tokens[0].value) + " instead.")
            self.tokens.pop(0)
            variable_type = self.tokens.pop(0).value
        else:
            if self.tokens[0].type == self.token_types.COLON:
                self.tokens.pop(0)
                variable_type = self.tokens.pop(0).value
            else:
                variable_type = None
        if self.tokens[0].type == self.token_types.ASSIGN:
            self.tokens.pop(0)
            value = self.parse_expression()
            return VariableDeclaration(variable_name, variable_type, value)
        else:
            return VariableDeclaration(variable_name, variable_type, None)

    def parse_return_statement(self):
        self.tokens.pop(0)
        return ReturnStatement(self.parse_statement())

    def parse_variable_assignment(self):
        variable_name = self.tokens.pop(0).value
        if self.tokens[0].type not in [self.token_types.ASSIGN, self.token_types.MOD_EQ, self.token_types.PLUS_EQ, self.token_types.MINUS_EQ, self.token_types.MUL_EQ, self.token_types.DIV_EQ]:
            raise Exception("Expected assignment operator after variable name in variable assignment but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        value = self.parse_expression()
        return VariableAssignment(variable_name, value)

    def parse_if_statement(self):
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after if in if statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        condition = self.parse_expression()
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after if condition in if statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected { after if condition in if statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        body = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type in [self.token_types.VAR, self.token_types.IF, self.token_types.WHILE, self.token_types.FOR, self.token_types.RETURN, self.token_types.IDENTIFIER]:
                body.append(self.parse_statement())
            elif self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            else:
                raise Exception("Unexpected token " + str(self.tokens[0].value) + " in if statement body.")
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected } at the end of if statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        else_body = []
        if self.tokens[0].type == self.token_types.ELSE:
            self.tokens.pop(0)
            if self.tokens[0].type != self.token_types.LBRACE:
                raise Exception("Expected { after else in if statement but got " + str(self.tokens[0].value) + " instead.")
            self.tokens.pop(0)
            while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
                if self.tokens[0].type in [self.token_types.VAR, self.token_types.IF, self.token_types.WHILE, self.token_types.FOR, self.token_types.RETURN, self.token_types.IDENTIFIER]:
                    else_body.append(self.parse_statement())
                elif self.tokens[0].type == self.token_types.SEMICOLON:
                    self.tokens.pop(0)
                else:
                    raise Exception("Unexpected token " + str(self.tokens[0].value) + " in else statement body.")
            if self.tokens[0].type != self.token_types.RBRACE:
                raise Exception("Expected } at the end of else statement but got " + str(self.tokens[0].value) + " instead.")
            self.tokens.pop(0)
        return IfStatement(condition, body, else_body)

    def parse_while_statement(self):
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after while in while statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        condition = self.parse_expression()
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after while condition in while statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected { after while condition in while statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        body = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type in [self.token_types.VAR, self.token_types.IF, self.token_types.WHILE, self.token_types.FOR, self.token_types.RETURN, self.token_types.IDENTIFIER]:
                body.append(self.parse_statement())
            elif self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            else:
                raise Exception("Unexpected token " + str(self.tokens[0].value) + " in while statement body.")
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected } at the end of while statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        return WhileStatement(condition, body)

    def parse_for_statement(self):
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after for in for statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        initializer = self.parse_statement()
        if self.tokens[0].type != self.token_types.SEMICOLON:
            raise Exception("Expected ; after for initializer in for statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        condition = self.parse_expression()
        if self.tokens[0].type != self.token_types.SEMICOLON:
            raise Exception("Expected ; after for condition in for statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        increment = self.parse_statement()
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after for increment in for statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.LBRACE:
            raise Exception("Expected { after for increment in for statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        body = []
        while self.tokens[0].type != self.token_types.RBRACE and self.tokens[0].type != self.token_types.EOF:
            if self.tokens[0].type in [self.token_types.VAR, self.token_types.IF, self.token_types.WHILE, self.token_types.FOR, self.token_types.RETURN, self.token_types.IDENTIFIER]:
                body.append(self.parse_statement())
            elif self.tokens[0].type == self.token_types.SEMICOLON:
                self.tokens.pop(0)
            else:
                raise Exception("Unexpected token " + str(self.tokens[0].value) + " in for statement body.")
        if self.tokens[0].type != self.token_types.RBRACE:
            raise Exception("Expected } at the end of for statement but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        return ForStatement(initializer, condition, increment, body)

    def parse_expression(self):
        if self.tokens[0].type == self.token_types.NEW:
            return self.parse_class_instantiation()
        elif self.tokens[0].type == self.token_types.IDENTIFIER:
            return self.parse_identifier()
        elif self.tokens[1].type == self.token_types.DOT:
            return self.parse_field_method_access()
        else:
            return self.parse_equality()

    def parse_class_instantiation(self):
        self.tokens.pop(0) # remove new token
        class_name = self.tokens.pop(0).value
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after class name in class instantiation " + str(class_name) + " but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        arguments = []
        while self.tokens[0].type != self.token_types.RPAREN:
            arguments.append(self.parse_expression())
            if self.tokens[0].type == self.token_types.COMMA:
                self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after class instantiation arguments but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        return ClassInstantiation(class_name, arguments)

    def parse_identifier(self):
        if self.tokens[1].type == self.token_types.LPAREN:
            return self.parse_function_call()
        elif self.tokens[1].type == self.token_types.ASSIGN:
            return self.parse_variable_assignment()
        elif self.tokens[1].type == self.token_types.DOT:
            return self.parse_field_method_access()
        else:
            return self.parse_equality()

    def parse_equality(self):
        left = self.parse_comparison()
        while self.tokens[0].type in [self.token_types.EQ, self.token_types.NEQ]:
            operator = self.tokens.pop(0).type
            right = self.parse_comparison()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.tokens[0].type in [self.token_types.GT, self.token_types.GTE, self.token_types.LT, self.token_types.LTE]:
            operator = self.tokens.pop(0).type
            right = self.parse_term()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.tokens[0].type in [self.token_types.PLUS, self.token_types.MINUS]:
            operator = self.tokens.pop(0).type
            right = self.parse_factor()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_factor(self):
        left = self.parse_primary()
        while self.tokens[0].type in [self.token_types.MUL, self.token_types.DIV]:
            operator = self.tokens.pop(0).type
            right = self.parse_primary()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_primary(self):
        if self.tokens[0].type in [self.token_types.INT, self.token_types.FLOAT, self.token_types.STRING, self.token_types.BOOLEAN]:
            return ValueNode(self.tokens.pop(0))
        elif self.tokens[0].type == self.token_types.LPAREN:
            self.tokens.pop(0)
            expression = self.parse_expression()
            if self.tokens[0].type != self.token_types.RPAREN:
                raise Exception("Expected ) after expression in primary but got " + str(self.tokens[0].value) + " instead.")
            self.tokens.pop(0)
            return expression
        else:
            return ValueNode(self.tokens.pop(0))

    def parse_field_method_access(self):
        instance = self.tokens.pop(0).value
        self.tokens.pop(0)
        if self.tokens[1].type == self.token_types.LPAREN:
            return self.parse_method_call(instance)
        else:
            return self.parse_field_access(instance)

    def parse_field_access(self, instance):
        field = self.tokens.pop(0).value
        return FieldAccess(instance, field)

    def parse_method_call(self, instance):
        method_name = self.tokens.pop(0).value
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after method name in method call but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        arguments = []
        while self.tokens[0].type != self.token_types.RPAREN and self.tokens[0].type != self.token_types.EOF:
            arguments.append(self.parse_expression())
            if self.tokens[0].type == self.token_types.COMMA:
                self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after method call arguments but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        return MethodCall(instance, method_name, arguments)

    def parse_function_call(self):
        function_name = self.tokens.pop(0).value
        if self.tokens[0].type != self.token_types.LPAREN:
            raise Exception("Expected ( after function name in function call but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        arguments = []
        while self.tokens[0].type != self.token_types.RPAREN and self.tokens[0].type != self.token_types.EOF:
            arguments.append(self.parse_expression())
            if self.tokens[0].type == self.token_types.COMMA:
                self.tokens.pop(0)
        if self.tokens[0].type != self.token_types.RPAREN:
            raise Exception("Expected ) after function call arguments but got " + str(self.tokens[0].value) + " instead.")
        self.tokens.pop(0)
        return FunctionCall(function_name, arguments)
