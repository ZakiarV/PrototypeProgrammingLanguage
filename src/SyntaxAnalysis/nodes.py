class ProgramNode:
    def __init__(self, body_ast):
        self.body_ast = body_ast

    def dictionary(self):
        return {
            "node_type": "ProgramNode",
            "body_ast": [ast.dictionary() for ast in self.body_ast]
        }

    def __repr__(self):
        return f"ProgramNode(Body: {self.body_ast})"


class ClassDeclaration:
    def __init__(self, class_name, extends_class_name, fields, methods, constructor=None):
        self.class_name = class_name
        self.extends_class_name = extends_class_name
        self.constructor = constructor
        self.fields = fields
        self.methods = methods

    def dictionary(self):
        return {"node_type": "ClassDeclaration", "data": {
            "class_name": self.class_name,
            "extends_class_name": self.extends_class_name,
            "constructor": self.constructor.dictionary() if self.constructor else None,
            "fields": [field.dictionary() for field in self.fields],
            "methods": [method.dictionary() for method in self.methods]
        }
                }

    def __repr__(self):
        return f"ClassDeclaration(Name: {self.class_name}, Extends: {self.extends_class_name}, Fields: {self.fields}, Methods: {self.methods})"


class FunctionDeclaration:
    def __init__(self, function_name, parameters, body_ast):
        self.function_name = function_name
        self.parameters = parameters
        self.body_ast = body_ast

    def dictionary(self):
        return {"node_type": "FunctionDeclaration", "data":
            {
                "function_name": self.function_name,
                "parameters": [parameter.dictionary() for parameter in self.parameters],
                "body_ast": [ast.dictionary() for ast in self.body_ast]
            }
                }

    def __repr__(self):
        return f"FunctionDeclaration(Name: {self.function_name}, Parameters: {self.parameters}, Body: {self.body_ast})"


class VariableDeclaration:
    def __init__(self, variable_name, variable_type, initial_value=None):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.initial_value = initial_value

    def dictionary(self):
        return {
            "node_type": "VariableDeclaration",
            "data": {
                "variable_name": self.variable_name,
                "variable_type": self.variable_type,
                "initial_value": self.initial_value.dictionary() if self.initial_value else None
            }
        }

    def __repr__(self):
        return f"VariableDeclaration(Name: {self.variable_name}, Type: {self.variable_type}, Initial Value: {self.initial_value})"


class VariableAssignment:
    def __init__(self, variable_name, expression):
        self.variable_name = variable_name
        self.expression = expression

    def dictionary(self):
        return {
            "node_type": "VariableAssignment",
            "data": {
                "variable_name": self.variable_name,
                "expression": self.expression.dictionary()
            }
        }

    def __repr__(self):
        return f"VariableAssignment(Variable: {self.variable_name}, Expression: {self.expression})"


class BinaryOperationNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        self.operator = operator

    def dictionary(self):
        return {
            "node_type": "BinaryOperationNode",
            "data": {
                "left": self.left.dictionary(),
                "operator": self.operator,
                "right": self.right.dictionary()
            }
        }

    def __repr__(self):
        return f"BinaryOperationNode(Left: {self.left}, Operator: {self.operator}, Right: {self.right})"


class IfStatement:
    def __init__(self, condition, body_ast, else_body_ast):
        self.condition = condition
        self.body_ast = body_ast
        self.else_body_ast = else_body_ast

    def dictionary(self):
        return {
            "node_type": "IfStatement",
            "data": {
                "condition": self.condition.dictionary(),
                "body_ast": [ast.dictionary() for ast in self.body_ast],
                "else_body_ast": [ast.dictionary() for ast in self.else_body_ast]
            }
        }

    def __repr__(self):
        return f"IfStatement(Condition: {self.condition}, Body: {self.body_ast}, Else Body: {self.else_body_ast})"


class WhileStatement:
    def __init__(self, condition, body_ast):
        self.condition = condition
        self.body_ast = body_ast

    def dictionary(self):
        return {
            "node_type": "WhileStatement",
            "data": {
                "condition": self.condition.dictionary(),
                "body_ast": [ast.dictionary() for ast in self.body_ast]
            }
        }

    def __repr__(self):
        return f"WhileStatement(Condition: {self.condition}, Body: {self.body_ast})"


class ForStatement:
    def __init__(self, initializer, condition, increment, body_ast):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body_ast = body_ast

    def dictionary(self):
        return {
            "node_type": "ForStatement",
            "data": {
                "initializer": self.initializer.dictionary(),
                "condition": self.condition.dictionary(),
                "increment": self.increment.dictionary(),
                "body_ast": [ast.dictionary() for ast in self.body_ast]
            }
        }

    def __repr__(self):
        return f"ForStatement(Initializer: {self.initializer}, Condition: {self.condition}, Increment: {self.increment}, Body: {self.body_ast})"


class ValueNode:
    def __init__(self, token):
        self.token = token

    def dictionary(self):
        return {
            "node_type": "ValueNode",
            "data": {
                "type": self.token.type,
                "value": self.token.value
            }
        }

    def __repr__(self):
        return f"ValueNode(Value: {self.token})"


class FunctionCall:
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments

    def dictionary(self):
        return {
            "node_type": "FunctionCall",
            "data": {
                "function_name": self.function_name,
                "arguments": [arg.dictionary() for arg in self.arguments]
            }
        }

    def __repr__(self):
        return f"FunctionCall(Function: {self.function_name}, Arguments: {self.arguments})"


class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

    def dictionary(self):
        return {
            "node_type": "ReturnStatement",
            "data": {
                "expression": self.expression.dictionary()
            }
        }

    def __repr__(self):
        return f"ReturnStatement(Expression: {self.expression})"


class ClassInstantiation:
    def __init__(self, class_name, arguments):
        self.class_name = class_name
        self.arguments = arguments

    def dictionary(self):
        return {
            "node_type": "ClassInstantiation",
            "data": {
                "class_name": self.class_name,
                "arguments": [arg.dictionary() for arg in self.arguments]
            }
        }

    def __repr__(self):
        return f"ClassInstantiation(Class: {self.class_name}, Arguments: {self.arguments})"


class FieldAccess:
    def __init__(self, instance, field_name):
        self.instance = instance
        self.field_name = field_name

    def dictionary(self):
        return {
            "node_type": "FieldAccess",
            "data": {
                "instance": self.instance.dictionary(),
                "field_name": self.field_name
            }
        }

    def __repr__(self):
        return f"FieldAccess(Instance: {self.instance}, Field: {self.field_name})"


class MethodCall:
    def __init__(self, instance, method_name, arguments):
        self.instance = instance
        self.method_name = method_name
        self.arguments = arguments

    def dictionary(self):
        return {
            "node_type": "MethodCall",
            "data": {
                "instance": self.instance.dictionary(),
                "method_name": self.method_name,
                "arguments": [arg.dictionary() for arg in self.arguments]
            }
        }

    def __repr__(self):
        return f"MethodCall(Instance: {self.instance}, Method: {self.method_name}, Arguments: {self.arguments})"


class ClassConstructor:
    def __init__(self, class_name, parameters, body_ast):
        self.class_name = class_name
        self.parameters = parameters
        self.body_ast = body_ast

    def dictionary(self):
        return {"node_type": "ClassConstructor", "data":
            {
                "class_name": self.class_name,
                "parameters": [parameter.dictionary() for parameter in self.parameters],
                "body_ast": [ast.dictionary() for ast in self.body_ast]
            }
                }

    def __repr__(self):
        return f"ClassConstructor(Name: {self.class_name}, Parameters: {self.parameters}, Body: {self.body_ast})"
