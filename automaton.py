from symbol_table import SymbolTable


class Automaton:

    def __init__(self):
        self.state = 1
        self.lexema = ""
        self.token_list = []
        self.current_line = 1
        self.current_column = 1
        self.symbol_table = SymbolTable()

    def verify_lexema(self, char):
        self.current_column = self.current_column + 1

        # Reconhece o char inicial e atribui um estado para resolve-lo
        if self.state == 1:
            if char == '':
                return False
            if char == ' ' or char == '\t' or char == '\r':
                self.state = 1 
            elif char == '\n':
                self.current_line = self.current_line + 1
                self.current_column = 1
                self.state = 1 
            elif char == '=':
                self.state = 9
            elif char == '-':
                self.lexema += char
                self.state = 3
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
        
        elif self.state == 3:
            if len(self.token_list) > 0:
                if "NUM" in self.token_list[len(self.token_list) - 1]:
                    if char == '-':
                        self.lexema += char
                    else:
                        if self.lexema.count('-') == 1:
                            self.state = 1
                            self.lexema = ""
                            self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            return True
                        else:
                            for i in range(self.lexema.count('-')-1):
                                self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            self.state = 1
                            self.lexema = ""
                            self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            return True
                else:
                    if char == '-':
                        self.lexema += char
                    else:
                        if self.lexema.count('-') == 1: 
                            self.state = 1
                            self.lexema = ""
                            self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            return True
                        else:
                            for i in range(self.lexema.count('-')-1):
                                self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            self.state = 1
                            self.lexema = ""
                            self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            return True
            else:
                if char == '-':
                    self.lexema += char
                else:
                    if self.lexema.count('-') == 1:
                        self.state = 1
                        self.lexema = ""
                        self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        return True
                    else:
                        for i in range(self.lexema.count('-')-1):
                            self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        self.state = 1
                        self.lexema = ""
                        self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        return True

        # Reconehceu o char '!' e espera um '=' para retornar o token 'diferente' - se não sinaliza erro lexico
        elif self.state == 6:
            if char == '=':
                self.state = 1
                self.token_list.append("<OP_DIFFERENT, !=> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                return False
            else:
                self.signals_lexico_error("Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))
        
        # Reconehceu o char '=' e espera um '=' para retornar o token 'igual' - se não retorna o token 'atribuição'
        elif self.state == 9:
            if char == '=':
                self.state = 1
                self.token_list.append("<OP_EQUAL, ==> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                return False
            else:
               self.state = 1
               self.current_column = self.current_column - 1
               self.token_list.append("<OP_ASSIGN, => - line: " + str(self.current_line) + ", column: " + str(self.current_column))
               return True
        
        # Reconehceu o char '>' e espera um '=' para retornar o token 'maior igual' - se não retorna o token 'maior'
        elif self.state == 12:
            if char == '=':
                self.state = 1
                self.token_list.append("<OP_GREATER_EQUAL, >=> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                return False
            else:
               self.state = 1
               self.current_column = self.current_column - 1
               self.token_list.append("<OP_GREATER, >> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
               return True
        
        # Reconehceu o char '<' e espera um '=' para retornar o token 'menor igual' - se não retorna o token 'menor'
        elif self.state == 15:
            if char == '=':
                self.state = 1
                self.token_list.append("<OP_LESS_EQUAL, <=> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                return False
            else:
               self.state = 1
               self.current_column = self.current_column - 1
               self.token_list.append("<OP_LESS, <> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
               return True
        
        # Reconehceu um char alfanumerico e concatena no lexema ate que outro char não alfanumerico seja reconhecido e então retorna um token 'id'
        elif self.state == 18:
            if char.isalnum():
                self.lexema += char
            else:
                self.state = 1
                self.current_column = self.current_column - 1
                self.token_list.append(self.symbol_table.add_lexema(self.lexema) + " - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                self.lexema = ""
                return True
        
        # Reconehceu um char numerico e concatena no lexema ate que outro char não numerico seja reconhecido e então retorna um token 'num'
        elif self.state == 25:
            if char.isdigit():
               self.lexema += char
            else:
                self.state = 1
                self.current_column = self.current_column - 1
                self.token_list.append("<NUM, " + self.lexema + "> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                self.lexema = ""
                return True
        
        return False

    def print_symbol_table(self):
        self.symbol_table.print_symbol_table()

    def get_token_list(self):
        return self.token_list

    def signals_lexico_error(self, message):
        print("[Erro Lexico]: ", message, "\n")