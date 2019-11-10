import sys
from tag import Tag

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo

    def sinalizaErroSintatico(self, message):
        print(f'[Erro Sintatico] na linha "{str(self.token.getLinha())}" e coluna "{str(self.token.getColuna())}":')
        print(message, "\n")

    def advance(self):
        print(f'[DEBUG] token: {self.token.toString()}')
        self.token = self.lexer.proxToken()

    def skip(self, message):
        self.sinalizaErroSintatico(message)
        self.advance()

    # verifica token esperado t 
    def eat(self, t):
        if(self.token.getNome() == t):
            self.advance()
            return True
        else:
            return False

    # Programa -> Classe EOF
    def Programa(self):
        self.Classe()

        if(self.token.getNome() != Tag.EOF):
            self.sinalizaErroSintatico(f'Era esperado "EOF", encontrado "{self.token.getLexema()}"')

    def Classe(self):
        if self.eat(Tag.KW_CLASS): 
            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')

            self.ListaFuncao()
            self.Main()

            if not self.eat(Tag.KW_END) :
                self.sinalizaErroSintatico(f'Era esperado "end", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_POINT):
                self.sinalizaErroSintatico(f'Era esperado ".", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(Classe)
            if(self.token.getNome() == Tag.EOF):
                self.sinalizaErroSintatico(f'Esperado "EOF", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Classe)
            else:
                self.skip(f'Esperado "EOF", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Classe()

    def DeclaraID(self):
        if self.token.getNome == Tag.KW_BOOL or self.token.getNome == Tag.KW_INTEGER or self.token.getNome == Tag.KW_STRING or self.token.getNome == Tag.KW_DOUBLE or self.token.getNome == Tag.KW_VOID:
            self.TipoPrimitivo()

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(DeclaraID)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID, END, RETURN, IF, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (DeclaraID)
            else:
                self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID, END, RETURN, IF, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.DeclaraID()

    def ListaFuncao(self):
        if self.token.getNome == Tag.KW_DEF:
            self.ListaFuncaoLine()
        # skip: (ListaFuncao)
        else:
            self.skip(f'Esperado "DEF", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaFuncao()

    def ListaFuncaoLine(self):
        if self.token.getNome == Tag.KW_DEF:
            self.Funcao()
            self.ListaFuncaoLine
        # skip: (ListaFuncaoLine)
        else:
            self.skip(f'Esperado "DEF", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaFuncaoLine()
    
    def Funcao(self):
        if self.eat(Tag.KW_DEF): 
            self.TipoPrimitivo()

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')

            self.ListaArg()

            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')

            self.RegexDeclaraID()
            self.ListaCmd()
            self.Retorno()

            if not self.eat(Tag.KW_END):
                self.sinalizaErroSintatico(f'Era esperado "END", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
        # synch: FOLLOW(Funcao)
            if self.token.getNome() == Tag.KW_DEFSTATIC:
                self.sinalizaErroSintatico(f'Esperado "DEF, DEFSTATIC", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Funcao)
            else:
                self.skip(f'Esperado "DEF, DEFSTATIC", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Funcao()

    def RegexDeclaraID(self):
        if self.token.getNome == Tag.KW_BOOL or self.token.getNome == Tag.KW_INTEGER or self.token.getNome == Tag.KW_STRING or self.token.getNome == Tag.KW_DOUBLE or self.token.getNome == Tag.KW_VOID:
            self.DeclaraID()
            
            self.RegexDeclaraID()
        # skip: (RegexDeclaraID)
        else:
            self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Funcao()
                
    def ListaArg(self):
        if self.token.getNome == Tag.KW_BOOL or self.token.getNome == Tag.KW_INTEGER or self.token.getNome == Tag.KW_STRING or self.token.getNome == Tag.KW_DOUBLE or self.token.getNome == Tag.KW_VOID:
            self.Arg()
            
            self.ListaArgLine()
        else:
        # synch: FOLLOW(ListaArg)
            if self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES:
                self.sinalizaErroSintatico(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, )", encontrado "{self.token.getLexema()}"')
                return
            # skip: (ListaArg)
            else:
                self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, )", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.ListaArg()
                    
    