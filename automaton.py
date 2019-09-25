from symbol_table import SymbolTable
import sys

class Automaton:

    def __init__(self):
        self.state = 1
        self.lexema = ""
        self.token_list = []
        self.current_line = 1
        self.current_column = 1
        self.cont_erros = 0
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
            elif char == '+':
                self.token_list.append("<OP_SUM, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '-':
                self.lexema += char
                self.state = 3
            elif char == '*':
                self.token_list.append("<OP_MULTIPLICATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '/':
                self.token_list.append("<OP_DIVISION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '!':
                self.state = 6
            elif char == '=':
                self.state = 9
            elif char == '>':
                self.state = 12
            elif char == '<':
                self.state = 15
            elif char == '/':
                self.state = 16
            elif char.isalpha():
                self.lexema += char
                self.state = 18
            elif char.isdigit():
                self.lexema += char
                self.state = 20
            elif char == ':':
                self.token_list.append("<CHAR_TWO_POINTS, :> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == ',':
                self.token_list.append("<CHAR_COMMA, ,> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '.':
                self.token_list.append("<CHAR_POINT, .> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == ';':
                self.token_list.append("<CHAR_SEMICOLON, ;> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '(':
                self.token_list.append("<CHAR_OPEN_PARENTHESES, (> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == ')':
                self.token_list.append("<CHAR_CLOSE_PARENTHESES, )> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '{':
                self.token_list.append("<CHAR_OPEN_KEY, {> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '}':
                self.token_list.append("<CHAR_CLOSE_KEY, }> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            elif char == '#':
                self.state = 30
            elif char == '\"':
                self.lexema += char
                self.state = 34
            else:
                self.signals_lexico_error("Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))
        
        # Reconhece o char '-' e verifica se o token anterior é um integer, double ou string então retorna um token subtração, se não retorna um token negação
        elif self.state == 3:
            if len(self.token_list) > 0:
                if "INTEGER" in self.token_list[len(self.token_list) - 1] or "DOUBLE" in self.token_list[len(self.token_list) - 1] or "STRING" in self.token_list[len(self.token_list) - 1] or  "ID" in self.token_list[len(self.token_list) - 1]:
                    if char == '-':
                        self.lexema += char
                    else:
                        if self.lexema.count('-') == 1:
                            self.state = 1
                            self.lexema = ""
                            self.current_column = self.current_column - 1
                            self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            return True
                        else:
                            self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            for i in range(self.lexema.count('-') - 1):
                                self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column - self.lexema.count('-') + i))
                            self.state = 1
                            self.lexema = ""
                            self.current_column = self.current_column - 1
                            return True
                else:
                    if char == '-':
                        self.lexema += char
                    else:
                        if self.lexema.count('-') == 1: 
                            self.state = 1
                            self.lexema = ""
                            self.current_column = self.current_column - 1
                            self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                            return True
                        else:
                            for i in range(self.lexema.count('-')-1):
                                self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column - self.lexema.count('-') + i))
                            self.state = 1
                            self.lexema = ""
                            self.current_column = self.current_column - 1
                            return True
            else:
                if char == '-':
                    self.lexema += char
                else:
                    if self.lexema.count('-') == 1:
                        self.state = 1
                        self.lexema = ""
                        self.current_column = self.current_column - 1
                        self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        return True
                    else:
                        for i in range(self.lexema.count('-')-1):
                            self.token_list.append("<OP_SUBTRACTION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        self.state = 1
                        self.lexema = ""
                        self.current_column = self.current_column - 1
                        self.token_list.append("<OP_NEGATION, -> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        return True

        # Reconhece o char '!' e espera um '=' para retornar o token 'diferente' - se não sinaliza erro lexico
        elif self.state == 6:
            if char == '=':
                self.state = 1
                self.token_list.append("<OP_DIFFERENT, !=> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                return False
            else:
                self.signals_lexico_error("Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))
        
        # Reconhece o char '=' e espera um '=' para retornar o token 'igual' - se não retorna o token 'atribuição'
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
        
        # Reconhece o char '>' e espera um '=' para retornar o token 'maior igual' - se não retorna o token 'maior'
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
        
        # Reconhece o char '<' e espera um '=' para retornar o token 'menor igual' - se não retorna o token 'menor'
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
        
        # Reconhece um char alfanumerico e concatena no lexema ate que outro char não alfanumerico seja reconhecido e então retorna um token 'id'
        elif self.state == 18:
            if char.isalnum():
                self.lexema += char
            else:
                self.state = 1
                self.current_column = self.current_column - 1
                self.token_list.append(self.symbol_table.add_lexema(self.lexema) + " - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                self.lexema = ""
                return True
        
        # Reconhece um char numerico e concatena no lexema ate que outro char não numerico seja reconhecido, exeto char '.' que começa a reconhecer um token 'double', se não então retorna um token 'integer'
        elif self.state == 20:
            if char.isdigit():
               self.lexema += char
            elif char == '.':
                self.lexema += char
                self.state = 31
            else:
                self.state = 1
                self.current_column = self.current_column - 1
                self.token_list.append("<INTEGER, " + self.lexema + "> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                self.lexema = ""
                return True

        # Reconhece um char numerico e um char '.' continua concatenando no lexema ate que outro char não numerico seja reconhecido e então retorna um token 'double', caso nenhum char numerico seja reconhecido depois do char '.' retorno erro lexico
        elif self.state == 31:
            if char.isdigit():
               self.lexema += char
            else:
                if self.lexema[-1:] != '.':
                    self.state = 1
                    self.current_column = self.current_column - 1
                    self.token_list.append("<DOUBLE, " + self.lexema + "> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                    self.lexema = ""
                    return True
                else:
                    self.signals_lexico_error("Formato de numero decimal inválido [" + self.lexema + "] Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))

        # Reconheceu o char '#' e tudo o que vier depois sera ignorado como comentario ate que um \n seja reconhecido
        elif self.state == 30:
            if char == '\n' or char == '':
                self.state = 1
                self.current_line = self.current_line + 1

        # Reconheceu o char " e tudo o que vier depois sera concatenado no lexema ate que um outro char " seja reconhecido e então retorna uma string
        elif self.state == 34:
            if char != '\"':
                if char == '':
                    self.signals_lexico_error("String não fechada em: [" + self.lexema + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column - 1))
                    self.lexema = ""

                self.lexema += char
            else:
                self.lexema += char
                self.state = 1
                self.token_list.append("<STRING, " + self.lexema + "> - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                self.lexema = ""

        return False

    def print_symbol_table(self):
        self.symbol_table.print_symbol_table()

    def get_token_list(self):
        return self.token_list

    def signals_lexico_error(self, message):
        print("[Erro Lexico]: ", message, "\n")
        self.cont_erros = self.cont_erros + 1
        if self.cont_erros >= 5:
            sys.exit(0)