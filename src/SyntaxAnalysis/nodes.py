class ProgramNode:
    def __init__(self, body_ast):
        self.body_ast = body_ast

    def __repr__(self):
        return f"ProgramNode(Body: {self.body_ast})"


class ClassDeclaration:
    def __init__(self, class_name, extends_class_name, fields, methods):
        self.class_name = class_name
        self.extends_class_name = extends_class_name
        self.fields = fields
        self.methods = methods

    def __repr__(self):
        return f"ClassDeclaration(Name: {self.class_name}, Extends: {self.extends_class_name}, Fields: {self.fields}, Methods: {self.methods})"


class FunctionDeclaration:
    def __init__(self, function_name, parameters, body_ast):
        self.function_name = function_name
        self.parameters = parameters
        self.body_ast = body_ast

    def __repr__(self):
        return f"FunctionDeclaration(Name: {self.function_name}, Parameters: {self.parameters}, Body: {self.body_ast})"


class VariableDeclaration:
    def __init__(self, variable_name, variable_type, initial_value=None):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.initial_value = initial_value

    def __repr__(self):
        return f"VariableDeclaration(Name: {self.variable_name}, Type: {self.variable_type}, Initial Value: {self.initial_value})"