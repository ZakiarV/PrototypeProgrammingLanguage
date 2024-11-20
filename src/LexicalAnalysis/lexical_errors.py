class LexicalError(Exception):
    def __init__(self, message, file="NOT IMPLEMENTED", line="NOT IMPLEMENTED", column="NOT IMPLEMENTED"):
        self.message = message
        self.file = file
        self.line = line
        self.column = column

    def __str__(self):
        return f'\nLexical error: {self.message} in file {self.file} at line {self.line}, column {self.column}'


class InvalidCharacterError(LexicalError):
    def __init__(self, char, file="NOT IMPLEMENTED", line="NOT IMPLEMENTED", column="NOT IMPLEMENTED"):
        super().__init__(f"Invalid character '{char}'", file, line, column)
