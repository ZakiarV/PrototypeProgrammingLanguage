class ProgramNode:
    def __init__(self, body_ast):
        self.body_ast = body_ast

    def dictionary(self):
        return {
            "node_type": "ProgramNode",
            "body_ast": [ast.dictionary() for ast in self.body_ast if ast]
        }

    def __repr__(self):
        return f"ProgramNode({self.body_ast})"


class ClassDeclaration:
    def __init__(self, class_name, extends_class_name, fields, methods, constructor=None):
        self.class_name = class_name
        self.extends_class_name = extends_class_name
        self.constructor = constructor
        self.fields: list = fields
        self.methods = methods

    def dictionary(self):
        return {"node_type": "ClassDeclaration", "data": {
            "class_name": self.class_name,
            "extends_class_name": self.extends_class_name,
            "constructor": self.constructor.dictionary() if self.constructor else None,
            "fields": [field.dictionary() for field in self.fields if field],
            "methods": [method.dictionary() for method in self.methods if method]
        }
                }

    def __repr__(self):
        return f"ClassDeclaration({self.class_name}, {self.extends_class_name}, {self.fields}, {self.methods}, {self.constructor})"


class FunctionDeclaration:
    def __init__(self, function_name, parameters, body_ast, class_name=None):
        self.function_name = function_name
        self.parameters = parameters
        self.body_ast = body_ast
        self.class_name = class_name

    def dictionary(self):
        if self.class_name:
            return {"node_type": "MethodDeclaration", "data":
                {
                    "class_name": self.class_name,
                    "function_name": self.function_name,
                    "parameters": [parameter.dictionary() for parameter in self.parameters],
                    "body_ast": [ast.dictionary() for ast in self.body_ast]
                }
                    }
        return {"node_type": "FunctionDeclaration", "data":
            {
                "function_name": self.function_name,
                "parameters": [parameter.dictionary() for parameter in self.parameters],
                "body_ast": [ast.dictionary() for ast in self.body_ast]
            }
                }

    def __repr__(self):
        return f"FunctionDeclaration({self.function_name}, {self.parameters}, {self.body_ast}, {self.class_name})"


class VariableDeclaration:
    def __init__(self, variable_name, variable_type=None, initial_value=None, class_name=None, function_name=None, is_parameter=False):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.initial_value = initial_value
        self.class_name = class_name
        self.function_name = function_name
        self.is_parameter = is_parameter

    def dictionary(self):
        if self.function_name:
            if self.is_parameter:
                return {
                    "node_type": "ParameterDeclaration",
                    "data": {
                        "function_name": self.function_name,
                        "variable_name": self.variable_name,
                        "variable_type": self.variable_type,
                        "initial_value": self.initial_value.dictionary() if self.initial_value else None
                    }
                }
            return {
                "node_type": "FunctionVariableDeclaration",
                "data": {
                    "function_name": self.function_name,
                    "variable_name": self.variable_name,
                    "variable_type": self.variable_type,
                    "initial_value": self.initial_value.dictionary() if self.initial_value else None
                }
            }
        if self.class_name:
            return {
                "node_type": "FieldDeclaration",
                "data": {
                    "class_name": self.class_name,
                    "variable_name": self.variable_name,
                    "variable_type": self.variable_type,
                    "initial_value": self.initial_value.dictionary() if self.initial_value else None
                }
            }
        return {
            "node_type": "VariableDeclaration",
            "data": {
                "variable_name": self.variable_name,
                "variable_type": self.variable_type,
                "initial_value": self.initial_value.dictionary() if self.initial_value else None
            }
        }

    def __repr__(self):
        return f"VariableDeclaration({self.variable_name}, {self.variable_type}, {self.initial_value}, {self.class_name}, {self.function_name}, {self.is_parameter})"


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
        return f"VariableAssignment({self.variable_name}, {self.expression})"


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
        return f"BinaryOperationNode({self.left}, {self.operator}, {self.right})"


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
                "else_body_ast": [ast.dictionary() for ast in self.else_body_ast if ast]
            }
        }

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.body_ast}, {self.else_body_ast})"


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
        return f"WhileStatement({self.condition}, {self.body_ast})"


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
        return f"ForStatement({self.initializer}, {self.condition}, {self.increment}, {self.body_ast})"


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
        return f"ValueNode({self.token})"


class FunctionCall:
    def __init__(self, function_name, arguments, is_builtin=False):
        self.function_name = function_name
        self.arguments = arguments
        self.is_builtin = is_builtin

    def dictionary(self):
        return {
            "node_type": "FunctionCall",
            "data": {
                "function_name": self.function_name,
                "arguments": [arg.dictionary() for arg in self.arguments],
                "is_builtin": self.is_builtin
            }
        }

    def __repr__(self):
        return f"FunctionCall({self.function_name}, {self.arguments})"


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
        return f"ReturnStatement({self.expression})"


class ClassInstantiation:
    def __init__(self, class_name, arguments):
        self.class_name = class_name
        self.arguments = arguments

    def dictionary(self):
        return {
            "node_type": "ClassInstantiation",
            "data": {
                "class_name": self.class_name,
                "arguments": [arg.dictionary() for arg in self.arguments if arg]
            }
        }

    def __repr__(self):
        return f"ClassInstantiation({self.class_name}, {self.arguments})"


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
        return f"FieldAccess({self.instance}, {self.field_name})"


class MethodCall:
    def __init__(self, instance, method_name, arguments):
        self.instance = instance
        self.method_name = method_name
        self.arguments = arguments

    def dictionary(self):
        return {
            "node_type": "MethodCall",
            "data": {
                "instance": self.instance,
                "method_name": self.method_name,
                "arguments": [arg.dictionary() for arg in self.arguments]
            }
        }

    def __repr__(self):
        return f"MethodCall({self.instance}, {self.method_name}, {self.arguments})"


class ClassConstructor:
    def __init__(self, class_name, parameters, body_ast):
        self.class_name = class_name
        self.parameters = parameters
        self.body_ast = body_ast

    def dictionary(self):
        return {"node_type": "ClassConstructor", "data":
            {
                "class_name": self.class_name,
                "parameters": [parameter.dictionary() for parameter in self.parameters if parameter],
                "body_ast": [ast.dictionary() for ast in self.body_ast]
            }
                }

    def __repr__(self):
        return f"ClassConstructor({self.class_name}, {self.parameters}, {self.body_ast})"
