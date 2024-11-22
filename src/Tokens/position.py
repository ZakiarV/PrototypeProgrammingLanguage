class Position:
    def __init__(self, line, start_pos):
        self.line = line
        self.start_pos = start_pos

    def advance(self, current_char):
        if current_char == "\n":
            self.line += 1
            self.start_pos = 0
        elif current_char == "\t":
            self.start_pos += 4
        else:
            self.start_pos += 1
        return Position(self.line, self.start_pos)

    def __sub__(self, other):
        return other.start_pos - self.start_pos

    def __repr__(self):
        return f"(line: {self.line}, column: {self.start_pos})"
