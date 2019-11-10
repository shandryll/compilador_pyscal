from symbol_table import SymbolTable
from token import Token
from tag import Tag
import sys

class Automaton:

    def __init__(self, input_file):
        try:
            self.input_file = open(input_file, 'rb')
            self.token_ant = ""
            self.lookahead = 0
            self.state = 1
            self.lexema = ""
            self.current_line = 1
            self.current_column = 1
            self.cont_erros = 0
            self.symbol_table = SymbolTable()
        except IOError: 
            print('Erro de abertura do arquivo. Encerrando.')
            sys.exit(0)

    def proxToken(self):
        self.state = 1
        self.lexema = ""
        char = '\u0000'

        while(True):
            self.lookahead = self.input_file.read(1)
            char = self.lookahead.decode('ascii')

            #self.current_column = self.current_column + 1

            # Reconhece o char inicial e atribui um estado para resolve-lo
            if self.state == 1:
                if char == '':
                    return Token(Tag.EOF, Tag.EOF, self.current_line, self.current_column)
                if char == ' ' or char == '\t' or char == '\r':
                    self.state = 1 
                elif char == '\n':
                    self.current_line = self.current_line + 1
                    self.current_column = 1
                    self.state = 1 
                elif char == '+':
                    return Token(Tag.OP_SUM, "+", self.current_line, self.current_column)
                elif char == '-':
                    self.lexema += char
                    self.state = 3
                elif char == '*':
                    return Token(Tag.OP_MULTIPLICATION, "*", self.current_line, self.current_column)
                elif char == '/':
                    return Token(Tag.OP_DIVISION, "/", self.current_line, self.current_column)
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
                    return Token(Tag.CHAR_TWO_POINTS, ":",  self.current_line, self.current_column)
                elif char == ',':
                    return Token(Tag.CHAR_COMMA, ",", self.current_line, self.current_column)
                elif char == '.':
                    return Token(Tag.CHAR_POINT, ".", self.current_line, self.current_column)
                elif char == ';':
                    return Token(Tag.CHAR_SEMICOLON, ";", self.current_line, self.current_column)
                elif char == '(':
                    return Token(Tag.CHAR_OPEN_PARENTHESES, "(", self.current_line, self.current_column)
                elif char == ')':
                    return Token(Tag.CHAR_CLOSE_PARENTHESES, ")", self.current_line, self.current_column)
                elif char == '[':
                    return Token(Tag.CHAR_OPEN_SQUARE_BRACKETS, "[", self.current_line, self.current_column)
                elif char == ']':
                    return Token(Tag.CHAR_CLOSE_SQUARE_BRACKETS, "]", self.current_line, self.current_column)
                elif char == '{':
                    return Token(Tag.CHAR_OPEN_KEY, "{", self.current_line, self.current_column)
                elif char == '}':
                    return Token(Tag.CHAR_CLOSE_KEY, "}", self.current_line, self.current_column)
                elif char == '#':
                    self.state = 30
                elif char == '\"':
                    self.lexema += char
                    self.state = 34
                else:
                    self.signals_lexico_error("Caractere invalido [" + char + "] - line: " + str(self.current_line) + ", column: " + str(self.current_column))
            
            # Reconhece o char '-' e verifica se o token anterior é um integer, double ou string então retorna um token subtração, se não retorna um token negação
            elif self.state == 3:
                if Tag.INTEGER in self.token_ant.getNome() or Tag.DOUBLE in self.token_ant.getNome() or Tag.STRING in self.token_ant.getNome() or Tag.ID in self.token_ant.getNome():
                    self.retornaPonteiro()
                    self.lookahead = self.input_file.read(1)
                    char = self.lookahead.decode('ascii')
                    if char == '-':
                        self.state = 1
                        self.lexema = ""
                        self.current_column = self.current_column - 1
                        token = Token(Tag.OP_NEGATION, "-", self.current_line, self.current_column)
                        self.retornaPonteiro()
                        return token
                    else:
                        self.state = 1
                        self.lexema = ""
                        self.current_column = self.current_column - 1
                        token = Token(Tag.OP_SUBTRACTION, "-", self.current_line, self.current_column)
                        self.retornaPonteiro()
                        return token
                else:
                    self.state = 1
                    self.lexema = ""
                    self.current_column = self.current_column - 1
                    token = Token(Tag.OP_NEGATION, "-", self.current_line, self.current_column)
                    self.retornaPonteiro()
                    return token

            # Reconhece o char '!' e espera um '=' para retornar o token 'diferente' - se não sinaliza erro lexico
            elif self.state == 6:
                if char == '=':
                    self.state = 1
                    return Token(Tag.OP_DIFFERENT, "!=", self.current_line, self.current_column)
                else:
                    self.state = 1
                    self.current_column = self.current_column - 1
                    token = Token(Tag.OP_EXCLAMATION, "!", self.current_line, self.current_column)
                    self.retornaPonteiro()
                    return token
            
            # Reconhece o char '=' e espera um '=' para retornar o token 'igual' - se não retorna o token 'atribuição'
            elif self.state == 9:
                if char == '=':
                    self.state = 1
                    return Token(Tag.OP_EQUAL, "==", self.current_line, self.current_column)
                else:
                    self.state = 1
                    self.current_column = self.current_column - 1
                    token = Token(Tag.OP_ASSIGN, "=", self.current_line, self.current_column)
                    self.retornaPonteiro()
                    return token
            
            # Reconhece o char '>' e espera um '=' para retornar o token 'maior igual' - se não retorna o token 'maior'
            elif self.state == 12:
                if char == '=':
                    self.state = 1
                    return Token(Tag.OP_GREATER_EQUAL, ">=", self.current_line, self.current_column)
                else:
                    self.state = 1
                    self.current_column = self.current_column - 1
                    token = Token(Tag.OP_GREATER, ">", self.current_line, self.current_column)
                    self.retornaPonteiro()
                    return token
            
            # Reconhece o char '<' e espera um '=' para retornar o token 'menor igual' - se não retorna o token 'menor'
            elif self.state == 15:
                if char == '=':
                    self.state = 1
                    return Token(Tag.OP_LESS_EQUAL, "<=", self.current_line, self.current_column)
                else:
                    self.state = 1
                    self.current_column = self.current_column - 1
                    token = Token(Tag.OP_LESS, "<", self.current_line, self.current_column)
                    self.retornaPonteiro()
                    return token
            
            # Reconhece um char alfanumerico e concatena no lexema ate que outro char não alfanumerico seja reconhecido e então retorna um token 'id'
            elif self.state == 18:
                if char.isalnum():
                    self.lexema += char
                else:
                    self.state = 1
                    self.current_column = self.current_column - 1
                    token = self.ts.getToken(lexema)
                    token.setLinha(self.current_line)
                    token.setColuna(self.current_column)
                    if(token is None):
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    self.lexema = ""
                    self.retornaPonteiro()
                    self.token_ant = token
                    return token
            
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
                    token = Token(Tag.INTEGER, self.lexema, self.current_line, self.current_column)
                    self.lexema = ""
                    self.retornaPonteiro()
                    self.token_ant = token
                    return token

            # Reconhece um char numerico e um char '.' continua concatenando no lexema ate que outro char não numerico seja reconhecido e então retorna um token 'double', caso nenhum char numerico seja reconhecido depois do char '.' retorno erro lexico
            elif self.state == 31:
                if char.isdigit():
                    self.lexema += char
                else:
                    if self.lexema[-1:] != '.':
                        self.state = 1
                        self.current_column = self.current_column - 1
                        token = Token(Tag.DOUBLE, self.lexema, self.current_line, self.current_column)
                        self.lexema = ""
                        self.retornaPonteiro()
                        self.token_ant = token
                        return token
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
                    if self.lexema[-1:] != '\"':
                        self.lexema += char
                        self.state = 1
                        token = Token(Tag.STRING, self.lexema, self.current_line, self.current_column)
                        self.lexema = ""
                        self.token_ant = token
                        return token
                    else:
                        self.signals_lexico_error("String vazia - line: " + str(self.current_line) + ", column: " + str(self.current_column))
                        self.lexema = ""
                        self.state = 1

    def print_symbol_table(self):
        self.symbol_table.print_symbol_table()

    def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro dao fechar arquivo. Encerrando.')
            sys.exit(0)

    def retornaPonteiro(self):
        if(self.lookahead.decode('ascii') != ''):
            self.input_file.seek(self.input_file.tell()-1)

    def signals_lexico_error(self, message):
        print("[Erro Lexico]: ", message, "\n")
        self.cont_erros = self.cont_erros + 1
        if self.cont_erros >= 5:
            sys.exit(0)
