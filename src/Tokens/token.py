class Token:
    def __init__(self, type_, value, start_pos=None, end_pos=None):
        self.type = type_
        self.value = value
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __repr__(self):
        return f"Token({self.type}, {self.value}, ({self.start_pos}, {self.end_pos}))"
