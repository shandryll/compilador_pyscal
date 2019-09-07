from symbol_table import SymbolTable


class Automaton:

    def __init__(self):
        self.state = 1
        self.lexema = ""
        self.current_line = 1
        self.current_column = 1
        self.symbol_table = SymbolTable()

    def verify_automaton(self, char):

        if not char == '\n':
            if not char:
                print(self.symbol_table.add_lexema(self.lexema) + " - line: " + str(self.current_line) + ", column: " + str(self.current_column) + '>')
                return True

            elif char == ' ':
                print(self.symbol_table.add_lexema(self.lexema) + " - line: " + str(self.current_line) + ", column: " + str(self.current_column) + '>')
                self.lexema = ''

            else:
                self.lexema = self.lexema + char

            self.current_column = self.current_column + 1

        elif char == '\n':
            print(self.symbol_table.add_lexema(self.lexema) + " - line: " + str(self.current_line) + ", column: " + str(self.current_column) + '>')
            self.lexema = ''
            self.current_column = 1
            self.current_line = self.current_line + 1

        return False



'''

        while True:
            if state == 1:
                if char == '':
                    print
                    'EOF'
                    break
                elif char == ' ' or char == '\t' or char == '\n' or char == '\r':
                    self.state = 1

'''