class TypeValueNode:
    def __init__(self, type_name, node):
        self.type = type_name
        self.node = node

    def dictionary(self):
        return {"node_type": "Value", "data": {
            "type": self.type
            }
        }

    def __str__(self):
        return f"{self.type}"


class TypeBinaryOperationNode:
    def __init__(self, type_left, operator, type_right, node):
        self.type_left = type_left
        self.operator = operator
        self.type_right = type_right
        self.node = node

    def dictionary(self):
        return {"node_type": "BinaryOperation", "data": {
            "type_left": self.type_left.dictionary(),
            "operator": self.operator,
            "type_right": self.type_right.dictionary()
            }
        }

    def __str__(self):
        return f"{self.type_left} {self.operator} {self.type_right}"


class TypeFunctionDeclaration:
    def __init__(self, return_type, function_name, parameters, body, node):
        self.type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.body = body
        self.node = node

    def dictionary(self):
        return {"node_type": "FunctionDeclaration", "data": {
            "return_type": self.type,
            "function_name": self.function_name,
            "parameters": [parameter.dictionary() for parameter in self.parameters],
            "body": [node.dictionary() for node in self.body]
            }
        }


class TypeMethodDeclaration:
    def __init__(self, return_type, class_name, method_name, parameters, body, node):
        self.type = return_type
        self.class_name = class_name
        self.method_name = method_name
        self.parameters = parameters
        self.body = body
        self.node = node

    def dictionary(self):
        return {"node_type": "MethodDeclaration", "data": {
            "return_type": self.type,
            "class_name": self.class_name,
            "method_name": self.method_name,
            "parameters": [parameter.dictionary() for parameter in self.parameters],
            "body": [node.dictionary() for node in self.body]
            }
        }


class TypeVariableDeclaration:
    def __init__(self, variable_name, variable_type, initialization_type, node):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.initialization_type = initialization_type
        self.node = node

    def dictionary(self):
        return {"node_type": "VariableDeclaration", "data": {
            "variable_name": self.variable_name,
            "variable_type": self.variable_type,
            "initialization_type": self.initialization_type.dictionary() if self.initialization_type else self.initialization_type
            }
        }

    def __str__(self):
        return f"{self.variable_name}: {self.variable_type}, {self.initialization_type.dictionary() if self.initialization_type else self.initialization_type}"

class TypeVariableAssignment:
    def __init__(self, variable_name, variable_type, assignment_type, node):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.assignment_type = assignment_type
        self.node = node

    def dictionary(self):
        return {"node_type": "VariableAssignment", "data": {
            "variable_name": self.variable_name,
            "variable_type": self.variable_type,
            "assignment_type": self.assignment_type.dictionary()
            }
        }

    def __str__(self):
        return f"{self.variable_name}: {self.variable_type} = {self.assignment_type.dictionary()}"


class TypeMethodCall:
    def __init__(self, class_name, method_name, arguments, return_type, node):
        self.class_name = class_name
        self.method_name = method_name
        self.arguments = arguments
        self.type = return_type
        self.node = node

    def dictionary(self):
        return {"node_type": "MethodCall", "data": {
            "class_name": self.class_name,
            "method_name": self.method_name,
            "arguments": [argument.dictionary() for argument in self.arguments],
            "return_type": self.type
            }
        }


class TypeFunctionCall:
    def __init__(self, function_name, arguments, return_type, node):
        self.function_name = function_name
        self.arguments = arguments
        self.type = return_type
        self.node = node

    def dictionary(self):
        return {"node_type": "FunctionCall", "data": {
            "function_name": self.function_name,
            "arguments": [argument.dictionary() for argument in self.arguments],
            "return_type": self.type
            }
        }


class TypeReturnStatement:
    def __init__(self, return_type, expression, node):
        self.type = return_type
        self.expression = expression
        self.node = node

    def dictionary(self):
        return {"node_type": "ReturnStatement", "data": {
            "return_type": self.type,
            "expression": self.expression.dictionary() if self.expression else self.expression
            }
        }

    def __str__(self):
        return f"{self.type}: {self.expression.dictionary() if self.expression else self.expression}"


class TypeClassInstantiation:
    def __init__(self, class_name, arguments, node):
        self.class_name, self.type = class_name, class_name
        self.arguments = arguments
        self.node = node

    def dictionary(self):
        return {"node_type": "Instantiation", "data": {
            "class_name": self.class_name,
            "arguments": [argument.dictionary() for argument in self.arguments]
            }
        }


class TypeClassConstructor:
    def __init__(self, class_name, parameters, body, node):
        self.class_name, self.type = class_name, class_name
        self.parameters = parameters
        self.body = body
        self.node = node

    def dictionary(self):
        return {"node_type": "Constructor", "data": {
            "class_name": self.class_name,
            "parameters": [parameter.dictionary() for parameter in self.parameters],
            "body": [node.dictionary() for node in self.body]
            }
        }


class TypeFieldAccess:
    def __init__(self, class_name, field, field_type, node):
        self.class_name = class_name
        self.field = field
        self.type = field_type
        self.node = node

    def dictionary(self):
        return {"node_type": "FieldAccess", "data": {
            "class_name": self.class_name,
            "field": self.field,
            "type": self.type
            }
        }


class TypeFieldDeclaration:
    def __init__(self, class_name, field_name, field_type, field_value, node):
        self.class_name = class_name
        self.field_name = field_name
        self.type = field_type
        self.value = field_value
        self.node = node

    def dictionary(self):
        return {"node_type": "FieldDeclaration", "data": {
            "class_name": self.class_name,
            "field_name": self.field_name,
            "type": self.type,
            "value": self.value.dictionary()
            }
        }

    def __str__(self):
        return f"{self.class_name}.{self.field_name}: {self.type}, {self.value.dictionary()}"


class TypeIfStatement:
    def __init__(self, condition, body, else_body, node):
        self.condition = condition
        self.body = body
        self.node = node
        self.else_body = else_body

    def dictionary(self):
        return {"node_type": "IfStatement", "data": {
            "condition": self.condition.dictionary(),
            "body": [node.dictionary() for node in self.body],
            "else_body": [node.dictionary() for node in self.else_body]
            }
        }


class TypeWhileStatement:
    def __init__(self, condition, body, node):
        self.condition = condition
        self.body = body
        self.node = node

    def dictionary(self):
        return {"node_type": "WhileStatement", "data": {
            "condition": self.condition.dictionary(),
            "body": [node.dictionary() for node in self.body]
            }
        }


class TypeForStatement:
    def __init__(self, variable, condition, increment, body, node):
        self.variable = variable
        self.condition = condition
        self.increment = increment
        self.body = body
        self.node = node

    def dictionary(self):
        return {"node_type": "ForStatement", "data": {
            "variable": self.variable.dictionary(),
            "condition": self.condition.dictionary(),
            "increment": self.increment.dictionary(),
            "body": [node.dictionary() for node in self.body]
            }
        }
