class TokenTypes:
    def __init__(self):
        self.LPAREN = "LPAREN"
        self.RPAREN = "RPAREN"
        self.LBRACE = "LBRACE"
        self.RBRACE = "RBRACE"
        self.LBRACKET = "LBRACKET"
        self.RBRACKET = "RBRACKET"

        self.PLUS = "PLUS"
        self.MINUS = "MINUS"
        self.MUL = "MUL"
        self.DIV = "DIV"
        self.MOD = "MOD"
        self.POW = "POW"
        self.EQ = "EQ"
        self.NEQ = "NEQ"
        self.LT = "LT"
        self.LTE = "LTE"
        self.GT = "GT"
        self.GTE = "GTE"
        self.ASSIGN = "ASSIGN"

        self.COMMA = "COMMA"
        self.DOT = "DOT"
        self.COLON = "COLON"
        self.SEMICOLON = "SEMICOLON"

        self.IF = "IF"
        self.ELSE = "ELSE"
        self.WHILE = "WHILE"
        self.FOR = "FOR"
        self.RETURN = "RETURN"

        self.INT = "INT"
        self.FLOAT = "FLOAT"
        self.STRING = "STRING"
        self.IDENTIFIER = "IDENTIFIER"
        self.BOOLEAN = "BOOLEAN"

        self.PLUS_EQ = "PLUS_EQ"
        self.MINUS_EQ = "MINUS_EQ"
        self.MUL_EQ = "MUL_EQ"
        self.DIV_EQ = "DIV_EQ"
        self.MOD_EQ = "MOD_EQ"
        self.POW_EQ = "POW_EQ"

        self.AND = "AND"
        self.OR = "OR"
        self.NOT = "NOT"

        self.TRUE = "TRUE"
        self.FALSE = "FALSE"

        self.FUNCTION = "FUNCTION"
        self.CLASS = "CLASS"
        self.VAR = "VAR"

        self.NEW = "NEW"

        self.EOF = "EOF"

        self.KEYWORDS = {
            "if": self.IF,
            "else": self.ELSE,
            "while": self.WHILE,
            "for": self.FOR,
            "return": self.RETURN,
            "int": self.INT,
            "float": self.FLOAT,
            "string": self.STRING,
            "boolean": self.BOOLEAN,
            "true": self.TRUE,
            "false": self.FALSE,
            "function": self.FUNCTION,
            "class": self.CLASS,
            "var": self.VAR,
            "new": self.NEW
        }

        self.built_in_functions = {
            "print": "PRINT",
            "input": "INPUT",
            "wait": "WAIT",
            "str": "str",
            "int": "int",
            "float": "float",
            "bool": "bool"
        }

        self.types = {
            "int": "INT",
            "float": "FLOAT",
            "string": "STRING",
            "boolean": "BOOLEAN"
        }
