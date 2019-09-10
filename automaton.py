from symbol_table import SymbolTable


class Automaton:

    def __init__(self):
        self.state = 1
        self.lexema = ""
        self.current_line = 1
        self.current_column = 1
        self.symbol_table = SymbolTable()

    def verify_lexema(self, char):
        self.current_column = self.current_column + 1

        # State: 'initial'
        if self.state == 1:
            if char == '':
                return None, False
            if char == ' ' or char == '\t' or char == '\r':
                self.state = 1 
            elif char == '\n':
                self.current_line = self.current_line + 1
                self.current_column = 1
                self.state = 1 
            elif char == '=':
                self.state = 9
            elif char == '!':
                self.state = 6
            elif char == '<':
                self.state = 15
            elif char == '>':
                self.state = 12
            elif char.isdigit():
                self.lexema += char
                self.state = 25
            elif char.isalpha():
                self.lexema += char
                self.state = 18
            elif char == '/':
                self.state = 16
            else:
                self.signals_lexico_error("Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))
        
        # State: '='
        elif self.state == 6:
            if char == '=':
                self.state = 1
                return "<OP_DIFFERENT, !=> - line: " + str(self.current_line) + ", column: " + str(self.current_column), False
            else:
                self.signals_lexico_error("Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))
        
        elif self.state == 9:
            if char == '=':
                self.state = 1
                return "<OP_EQUAL, ==> - line: " + str(self.current_line) + ", column: " + str(self.current_column), False
            else:
               self.state = 1
               self.current_column = self.current_column - 1
               return "<OP_ASSIGN, => - line: " + str(self.current_line) + ", column: " + str(self.current_column), True
        
        elif self.state == 12:
            if char == '=':
                self.state = 1
                return "<OP_GREATER_EQUAL, >=> - line: " + str(self.current_line) + ", column: " + str(self.current_column), False
            else:
               self.state = 1
               self.current_column = self.current_column - 1
               return "<OP_GREATER, >> - line: " + str(self.current_line) + ", column: " + str(self.current_column), True
        
        elif self.state == 15:
            if char == '=':
                self.state = 1
                return "<OP_LESS_EQUAL, <=> - line: " + str(self.current_line) + ", column: " + str(self.current_column), False
            else:
               self.state = 1
               self.current_column = self.current_column - 1
               return "<OP_LESS, <> - line: " + str(self.current_line) + ", column: " + str(self.current_column), True
        
        # State: 'id'
        elif self.state == 18:
            if char.isalnum():
                self.lexema += char
            else:
                self.state = 1
                self.current_column = self.current_column - 1
                content = self.symbol_table.add_lexema(self.lexema) + " - line: " + str(self.current_line) + ", column: " + str(self.current_column)
                self.lexema = ""
                return content, True
        
        # State: 'number'
        elif self.state == 25:
            if char.isdigit():
               self.lexema += char
            else:
                self.state = 1
                self.current_column = self.current_column - 1
                content = "<NUM, " + self.lexema + "> - line: " + str(self.current_line) + ", column: " + str(self.current_column)
                self.lexema = ""
                return content, True
        
        return None, False

    def print_symbol_table(self):
        self.symbol_table.print_symbol_table()

    def signals_lexico_error(self, message):
        print("[Erro Lexico]: ", message, "\n")