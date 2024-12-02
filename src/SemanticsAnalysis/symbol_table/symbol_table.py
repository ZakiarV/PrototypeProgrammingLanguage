class BuiltInFunctionSymbolTable:
    def __init__(self):
        self.functions = {
            "print": "void",
            "input": "STRING",
            "int": "INT",
            "float": "FLOAT",
            "str": "STRING",
            "bool": "BOOLEAN",
            "wait": "void"
        }


class ForSymbolTable:
    def __init__(self, loop_variable, loop_variable_type, parent):
        self.loop_variable = loop_variable
        self.loop_variable_type = loop_variable_type
        self.built_in_functions = {}
        self.parent = parent
        self.scope_level = 0

    def update_scope_level(self, scope_level):
        self.scope_level = scope_level + 1

    def add_built_in_function(self, function_name):
        self.built_in_functions[function_name] = BuiltInFunctionSymbolTable().functions[function_name]

    def dictionary(self):
        dictionary = {
            "type": "ForSymbolTable",
            "data": {
                "loop_variable": self.loop_variable,
                "loop_variable_type": self.loop_variable_type,
                "parent": self.parent.name if isinstance(self.parent, ProgramSymbolTable) else self.parent.function_name,
                "scope_level": self.scope_level
            }
        }
        return dictionary

    def __repr__(self):
        return (f"ForSymbolTable(\n\t"
                f"\n\tLoop Variable: {self.loop_variable}, "
                f"\n\tParent: {self.parent.name}"
                f"\n\tScope Level: {self.scope_level})")


class FunctionSymbolTable:
    def __init__(self, function_name, parent):
        self.function_name = function_name
        self.parent = parent
        self.parameters = {}
        self.variables = {}
        self.for_loop_vars = {}
        self.built_in_functions = {}
        self.return_type = None
        self.scope_level = 0

    def add_parameter(self, parameter_name, parameter_type):
        self.parameters[parameter_name] = parameter_type

    def add_variable(self, variable_name, variable_type):
        self.variables[variable_name] = variable_type

    def add_for_loop_var(self, loop_variable, loop_variable_type):
        self.for_loop_vars[loop_variable] = ForSymbolTable(loop_variable, loop_variable_type, self)

    def update_scope_level(self, scope_level):
        self.scope_level = scope_level + 1

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_built_in_function(self, function_name):
        self.built_in_functions[function_name] = BuiltInFunctionSymbolTable().functions[function_name]
        if isinstance(self.parent, ProgramSymbolTable):
            self.parent.add_built_in_function(function_name)
        elif isinstance(self.parent, ClassSymbolTable):
            self.parent.parent.add_built_in_function(function_name)

    def get_variable(self, variable_name):
        if variable_name in self.variables:
            return self.variables[variable_name]
        return None

    def get_for_loop_var(self, loop_variable):
        if loop_variable in self.for_loop_vars:
            return self.for_loop_vars[loop_variable]
        return None

    def dictionary(self):
        dictionary = {
            "type": "FunctionSymbolTable",
            "data": {
                "function_name": self.function_name,
                "parent": self.parent.name,
                "scope_level": self.scope_level,
                "parameters": self.parameters,
                "variables": self.variables,
                "for_loop_vars": {loop_variable: loop_var.dictionary() for loop_variable, loop_var in self.for_loop_vars.items()},
                "return_type": self.return_type
            }
        }
        return dictionary

    def __repr__(self):
        return (f"FunctionSymbolTable(\n\t"
                f"\n\tName: {self.function_name}, "
                f"\n\tParent: {self.parent.name}"
                f"\n\tScope Level: {self.scope_level}, "
                f"\n\t\tParameters: {self.parameters}, "
                f"\n\t\tVariables: {self.variables},"
                f"\n\t\tFor Loop Variables: {self.for_loop_vars})")


class ClassSymbolTable:
    def __init__(self, class_name, parent):
        self.name = class_name
        self.parent = parent
        self.extends = None
        self.constructor = None
        self.fields = {}
        self.methods = {}
        self.scope_level = 0

    def set_extends(self, extends_class_name):
        self.extends = self.parent.class_declarations[extends_class_name] if extends_class_name in self.parent.class_declarations else None

    def set_constructors(self):
        self.constructor = FunctionSymbolTable("init", self)
        self.constructor.update_scope_level(self.scope_level)

    def add_field(self, field_name, field_type):
        self.fields[field_name] = field_type

    def add_method(self, method_name):
        self.methods[method_name] = FunctionSymbolTable(method_name, self)
        self.methods[method_name].update_scope_level(self.scope_level)

    def update_scope_level(self, scope_level):
        self.scope_level = scope_level + 1

    def dictionary(self):
        dictionary = {
            "type": "ClassSymbolTable",
            "data": {
                "class_name": self.name,
                "parent": self.parent.name,
                "extends": self.extends.name if self.extends else None,
                "scope_level": self.scope_level,
                "constructor": self.constructor.dictionary() if self.constructor else None,
                "fields": {field_name: field for field_name, field in self.fields.items()},
                "methods": {method_name: method.dictionary() for method_name, method in self.methods.items()}
            }
        }
        return dictionary

    def get_field(self, field_name):
        if field_name in self.fields:
            return self.fields[field_name]
        elif self.extends:
            return self.extends.get_field(field_name)
        return None

    def get_method(self, method_name):
        if method_name in self.methods:
            return self.methods[method_name]
        elif self.extends:
            return self.extends.get_method(method_name)
        return None

    def __repr__(self):
        return (f"ClassSymbolTable(\n\t"
                f"\n\tName: {self.name}, "
                f"\n\tParent: {self.parent.name}"
                f"\n\tScope Level: {self.scope_level}, "
                f"\n\t\tFields: {self.fields}, "
                f"\n\t\tMethods: {self.methods})")


class ProgramSymbolTable:
    def __init__(self, name="main", parent=None):
        self.name = name
        self.parent = parent
        self.global_built_in_functions = {}
        self.built_in_functions = {}
        self.variables = {}
        self.functions = {}
        self.for_loop_vars = {}
        self.class_declarations = {}
        self.scope_level = 0

    def add_variable(self, variable_name, variable_type):
        self.variables[variable_name] = variable_type

    def add_function(self, function_name):
        self.functions[function_name] = FunctionSymbolTable(function_name, self)
        self.functions[function_name].update_scope_level(self.scope_level)

    def add_class_declaration(self, class_name):
        self.class_declarations[class_name] = ClassSymbolTable(class_name, self)
        self.class_declarations[class_name].update_scope_level(self.scope_level)

    def add_for_loop_var(self, loop_variable, loop_variable_type):
        self.for_loop_vars[loop_variable] = ForSymbolTable(loop_variable, loop_variable_type, self)

    def get_variable(self, variable_name):
        if variable_name in self.variables:
            return self.variables[variable_name]
        return None

    def get_function(self, function_name):
        if function_name in self.functions:
            return self.functions[function_name]
        return None

    def get_for_loop_var(self, loop_variable):
        if loop_variable in self.for_loop_vars:
            return self.for_loop_vars[loop_variable]
        return None

    def get_class_declaration(self, class_name):
        if class_name in self.class_declarations:
            return self.class_declarations[class_name]
        return None

    def add_built_in_function(self, function_name):
        self.built_in_functions[function_name] = BuiltInFunctionSymbolTable().functions[function_name]
        self.global_built_in_functions[function_name] = self.built_in_functions[function_name]

    def dictionary(self):
        dictionary = {
            "type": "ProgramSymbolTable",
            "data": {
                "name": self.name,
                "parent": self.parent.name if self.parent else None,
                "scope_level": self.scope_level,
                "variables": self.variables,
                "functions": {function_name: function.dictionary() for function_name, function in self.functions.items()},
                "built_in_functions": self.built_in_functions,
                "global_built_in_functions": self.global_built_in_functions,
                "class_declarations": {class_name: class_.dictionary() for class_name, class_ in self.class_declarations.items()},
                "for_loop_vars": {loop_variable: loop_var.dictionary() for loop_variable, loop_var in self.for_loop_vars.items()}
            }
        }
        return dictionary

    def __repr__(self):
        return (f"SymbolTable("
                f"\n\tName: {self.name}, "
                f"\n\tParent: {self.parent.name if self.parent else None}"
                f"\n\tScope Level: {self.scope_level}, "
                f"\n\t\tVariables: {self.variables}, "
                f"\n\t\tFunctions: {self.functions}, "
                f"\n\t\tClasses: {self.class_declarations}",
                f"\n\t\tFor Loop Variables: {self.for_loop_vars}"
                f"\n)")
