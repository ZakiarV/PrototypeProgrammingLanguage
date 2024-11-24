from .lexical_errors import InvalidCharacterError

from ..Tokens.token import Token
from ..Tokens.token_types import TokenTypes
from..Tokens.position import Position


class Lexer:
    def __init__(self, source_code):
        self.source_code = list(source_code)
        self.tokens = []
        self.token_types = TokenTypes()

    def tokenize(self):
        while len(self.source_code) > 0:
            current_char = self.source_code.pop(0)

            if current_char in "\t\n ":
                pass
            elif current_char == "(":
                self.tokens.append(Token(self.token_types.LPAREN, "("))
            elif current_char == ")":
                self.tokens.append(Token(self.token_types.RPAREN, ")"))
            elif current_char == "{":
                self.tokens.append(Token(self.token_types.LBRACE, "{"))
            elif current_char == "}":
                self.tokens.append(Token(self.token_types.RBRACE, "}"))
            elif current_char == "[":
                self.tokens.append(Token(self.token_types.LBRACKET, "["))
            elif current_char == "]":
                self.tokens.append(Token(self.token_types.RBRACKET, "]"))
            elif current_char == "+":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.PLUS_EQ, "+="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.PLUS, "+"))
            elif current_char == "-":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.MINUS_EQ, "-="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.MINUS, "-"))
            elif current_char == "*":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.MUL_EQ, "*="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.MUL, "*"))
            elif current_char == "/":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.DIV_EQ, "/="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.DIV, "/"))
            elif current_char == "%":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.MOD_EQ, "%="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.MOD, "%"))
            elif current_char == "^":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.POW_EQ, "^="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.POW, "^"))
            elif current_char == "=":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.EQ, "=="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.ASSIGN, "="))
            elif current_char == "!":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.NEQ, "!="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.NOT, "!"))
            elif current_char == "<":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.LTE, "<="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.LT, "<"))
            elif current_char == ">":
                if self.source_code[0] == "=":
                    self.tokens.append(Token(self.token_types.GTE, ">="))
                    self.source_code.pop(0)
                else:
                    self.tokens.append(Token(self.token_types.GT, ">"))
            elif current_char == ",":
                self.tokens.append(Token(self.token_types.COMMA, ","))
            elif current_char == ".":
                self.tokens.append(Token(self.token_types.DOT, "."))
            elif current_char == ":":
                self.tokens.append(Token(self.token_types.COLON, ":"))
            elif current_char == ";":
                self.tokens.append(Token(self.token_types.SEMICOLON, ";"))
            elif current_char == '"':
                self.tokens.append(self.make_string())
            elif current_char.isnumeric():
                self.tokens.append(self.make_number(current_char))
            elif current_char.isalpha() or current_char == '_':
                self.tokens.append(self.make_identifier(current_char))
            else:
                raise InvalidCharacterError(current_char)

        self.tokens.append(Token(self.token_types.EOF, "EOF"))

        return self.tokens

    def make_string(self):
        string = ""
        while self.source_code[0] != '"' and len(self.source_code) > 0:
            string += self.source_code.pop(0)
        self.source_code.pop(0)
        return Token(self.token_types.STRING, string)

    def make_number(self, first_char):
        number = first_char
        dot_count = 0
        if len(self.source_code) == 0:
            return Token(self.token_types.INT, int(number))
        while (self.source_code[0].isnumeric() or self.source_code[0] == ".") and len(self.source_code) > 0:
            if self.source_code[0] == ".":
                dot_count += 1
                if dot_count > 1:
                    break
            number += self.source_code.pop(0)
            if len(self.source_code) == 0:
                break
        return Token(self.token_types.FLOAT if dot_count == 1 else self.token_types.INT,
                     float(number) if dot_count == 1 else int(number))

    def make_identifier(self, first_char):
        identifier = first_char
        if len(self.source_code) == 0:
            return Token(self.token_types.IDENTIFIER, identifier)
        else:
            while (self.source_code[0].isalnum() or self.source_code[0] == "_") and len(self.source_code) > 0:
                identifier += self.source_code.pop(0)

        if identifier in self.token_types.KEYWORDS:
            return Token(self.token_types.KEYWORDS[identifier], identifier)
        elif identifier in self.token_types.built_in_functions:
            return Token(self.token_types.built_in_functions[identifier], identifier)
        else:
            return Token(self.token_types.IDENTIFIER, identifier)
