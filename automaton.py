class Automaton:

    def __init__(self, state, char):
        self.state = state
        self.char = char

    def verify_automaton(self, state, char=None):
        while True:
            if state == 1:
                if char == '':
                    print
                    'EOF'
                    break
                elif char == ' ' or char == '\t' or char == '\n' or char == '\r':
                    self.state = 1

