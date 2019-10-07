class Token:
    END = 0
    MULTIPLE_CHOICE = 1
    Q_AND_A = 2
    LITERAL = 3

    def __init__(self, tok, value=None):
        self.tok = tok
        self.value = value