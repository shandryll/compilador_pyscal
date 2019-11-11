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
                self.sinalizaErroSintatico(f'Esperado "CLASS, EOF", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Classe)
            else:
                self.skip(f'Esperado "EOF", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Classe()

    def DeclaraID(self):
        if self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID:
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
        if self.token.getNome() == Tag.KW_DEF:
            self.ListaFuncaoLine()
        # skip: (ListaFuncao)
        else:
            self.skip(f'Esperado "DEF", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaFuncao()

    def ListaFuncaoLine(self):
        if self.token.getNome() == Tag.KW_DEF:
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
        if self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID:
            self.DeclaraID()
            
            self.RegexDeclaraID()
        # skip: (RegexDeclaraID)
        else:
            self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Funcao()
                
    def ListaArg(self):
        if self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID:
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
                    
    def ListaArgLine(self):
        if self.eat(Tag.CHAR_COMMA):
            self.ListaArg
        # skip: (ListaArgLine)
        else:
            self.skip(f'Esperado ",", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaArgLine()
                
    def Arg(self):
        if self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID:
            self.TipoPrimitivo()
            self.eat(Tag.ID)
        else:
        # synch: FOLLOW(Arg)
            if self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA:
                self.sinalizaErroSintatico(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ,, )", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Arg)
            else:
                self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ,, )", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Arg()
                    
    def Retorno(self):
        if self.eat(Tag.KW_RETURN):
            self.Expressao()
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado "RETURN, ;", encontrado "{self.token.getLexema()}"')
        # skip: (Retorno)
        else:
            self.skip(f'Esperado "RETURN, ;", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Retorno()
    
    def Main(self):
        if self.eat(Tag.KW_DEFSTATIC):
            if not self.eat(Tag.KW_VOID):
                self.sinalizaErroSintatico(f'Era esperado "VOID", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.KW_MAIN):
                self.sinalizaErroSintatico(f'Era esperado "MAIN", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.KW_STRING):
                self.sinalizaErroSintatico(f'Era esperado "STRING", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_OPEN_SQUARE_BRACKETS):
                self.sinalizaErroSintatico(f'Era esperado "[", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_CLOSE_SQUARE_BRACKETS):
                self.sinalizaErroSintatico(f'Era esperado "]", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')
            
            self.RegexDeclaraID()
            self.ListaCmd()
            
            if not self.eat(Tag.KW_END):
                self.sinalizaErroSintatico(f'Era esperado "END", encontrado "{self.token.getLexema()}"')    
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(Main)
            if self.token.getNome() == Tag.KW_END:
                self.sinalizaErroSintatico(f'Esperado "DEFSTATIC, END", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Main)
            else:
                self.skip(f'Esperado "DEFSTATIC, END", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Main()
                
    def TipoPrimitivo(self):
        if not self.eat(Tag.KW_BOOL) or not self.eat(Tag.KW_INTEGER) or not self.eat(Tag.KW_STRING) or not self.eat(Tag.KW_DOUBLE) or not self.eat(Tag.KW_VOID):
            # synch: FOLLOW(TipoPrimitivo)
            if self.token.getNome() == Tag.ID:
                self.sinalizaErroSintatico(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID", encontrado "{self.token.getLexema()}"')
                return
            # skip: (TipoPrimitivo)
            else:
                self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.TipoPrimitivo()
                    
    def ListaCmd(self):
        if self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE:
            self.ListaCmdLine()
        # skip: (ListaCmd)
        else:
            self.skip(f'Esperado "IF, WHILE, ID, WRITE", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaCmd()
                
    def ListaCmdLine(self):
        if self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE:
            self.Cmd()
            self.ListaCmdLine()
        # skip: (ListaCmdLine)
        else:
            self.skip(f'Esperado "IF, WHILE, ID, WRITE", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaCmdLine()
                
    def Cmd(self):
        if self.token.getNome() == Tag.KW_IF:
            self.CmdIf()
        elif self.token.getNome() == Tag.KW_WHILE:
            self.CmdWhile()
        elif self.eat(Tag.ID):
            self.CmdAtribFunc()
        elif self.token.getNome() == Tag.KW_WRITE:
            self.CmdWrite()
        else:
            # synch: FOLLOW(Cmd)
            if self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_ELSE:
                self.sinalizaErroSintatico(f'Esperado "IF, WHILE, ID, WRITE, END, RETURN, ELSE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Cmd)
            else:
                self.skip(f'Esperado "IF, WHILE, ID, WRITE, END, RETURN, ELSE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Cmd()
                    
    def CmdAtribFunc(self):
        if self.token.getNome() == Tag.OP_ASSIGN:
            self.CmdAtribui()
        elif self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.CmdFuncao()
        else:
            # synch: FOLLOW(CmdAtribFunc)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "=, (, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdAtribFunc)
            else:
                self.skip(f'Esperado "=, (, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdAtribFunc()
                    
    def CmdIf(self):
        if self.eat(Tag.KW_IF):
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')    
            
            self.Expressao()
            
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')      
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')
                
            self.Listacmd()
            self.CmdIfLine()
        else:
            # synch: FOLLOW(CmdIf)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "IF, ID, END, RETURN, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdIf)
            else:
                self.skip(f'Esperado "IF, ID, END, RETURN, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdIf()
            
    def CmdIfLine(self):
        if self.eat(Tag.KW_END):
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')    
        elif self.eat(Tag.KW_ELSE):
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')    
            
            self.ListaCmd()
                
            if not self.eat(Tag.KW_END):
                self.sinalizaErroSintatico(f'Era esperado "END", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(CmdIfLine)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "END, ELSE, ID, RETURN, IF, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdIfLine)
            else:
                self.skip(f'Esperado "END, ELSE, ID, RETURN, IF, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdIfLine()
                    
    def CmdWhile(self):
        if self.eat(Tag.KW_WHILE):
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')
            
            self.Expressao()    
              
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')
            
            self.ListaCmd()
            
            if not self.eat(Tag.KW_END):
                self.sinalizaErroSintatico(f'Era esperado "END", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(CmdWhile)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "WHILE, ID, END, RETURN, ELSE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdWhile)
            else:
                self.skip(f'Esperado "WHILE, ID, RETURN, IF, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdWhile()
                    
    def CmdWrite(self):
        if self.eat(Tag.KW_WRITE):
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')
            
            self.Expressao()    
              
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(CmdWrite)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE:
                self.sinalizaErroSintatico(f'Esperado "WRITE, ID, END, RETURN, ELSE, WHILE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdWrite)
            else:
                self.skip(f'Esperado "WRITE, ID, RETURN, IF, WHILE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdWrite()
                    
    def CmdAtribui(self):
        if self.eat(Tag.OP_ASSIGN):
            self.Expressao()
            
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')    
        else:
            # synch: FOLLOW(CmdAtribui)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "=, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdAtribui)
            else:
                self.skip(f'Esperado "=, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdAtribui()
                    
    def CmdFuncao(self):
        if self.eat(Tag.CHAR_OPEN_PARENTHESES):
            self.RegexExp()
            
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(CmdFuncao)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "(, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (CmdFuncao)
            else:
                self.skip(f'Esperado "(, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.CmdFuncao()
                    
    def RegexExp(self):
        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.Expressao()
            self.RegexExpLine()
        # skip: (RegexExp)
        else:
            self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.RegexExp()
                
    def RegexExpLine(self):
        if self.eat(Tag.CHAR_COMMA):
            self.Expressao()
            self.RegexExpLine()
        # skip: (RegexExpLine)
        else:
            self.skip(f'Esperado ",", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.RegexExpLine()
    
    def Expressao(self):
        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.Exp1()
            self.ExpLine()
        # skip: (Expressao)
        else:
            self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Expressao()
                
    def ExpLine(self):
        if self.eat(Tag.OP_OR):
            self.Exp1()
            self.ExpLine()
        elif self.eat(Tag.OP_AND):
            self.Exp1()
            self.ExpLine()
        # skip: (ExpLine)
        else:
            self.skip(f'Esperado "OR, AND", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ExpLine()
                
    def Exp1(self):
        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.Exp2()
            self.Exp1Line()
        else:
        # synch: FOLLOW(Exp1)
            if self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND:
                self.sinalizaErroSintatico(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Exp1)
            else:
                self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Exp1()
                    
    def Exp1Line(self):
        if self.eat(Tag.OP_LESS):
            self.Exp2()
            self.Exp1Line()
        elif self.eat(Tag.OP_LESS_EQUAL):
            self.Exp2()
            self.Exp1Line()
        elif self.eat(Tag.OP_GREATER):
            self.Exp2()
            self.Exp1Line()
        elif self.eat(Tag.OP_GREATER_EQUAL):
            self.Exp2()
            self.Exp1Line()
        elif self.eat(Tag.OP_EQUAL):
            self.Exp2()
            self.Exp1Line()
        elif self.eat(Tag.OP_DIFFERENT):
            self.Exp2()
            self.Exp1Line()
        # skip: (Exp1Line)
        else:
            self.skip(f'Esperado "<, <=, >, >=, ==, !=", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Exp1Line()
                
    def Exp2(self):
        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.Exp3()
            self.Exp2Line()
        else:
        # synch: FOLLOW(Exp2)
            if self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT:
                self.sinalizaErroSintatico(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Exp2)
            else:
                self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Exp2()
                    
    def Exp2Line(self):
        if self.eat(Tag.OP_SUM):
            self.Exp3()
            self.Exp2Line()
        elif self.eat(Tag.OP_SUBTRACTION):
            self.Exp3()
            self.Exp2Line()
        # skip: (Exp2Line)
        else:
            self.skip(f'Esperado "+, -", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Exp2Line()
                
    def Exp3(self):
        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.Exp4()
            self.Exp3Line()
        else:
        # synch: FOLLOW(Exp3)
            if self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT or self.token.getNome() == Tag.OP_SUM or self.token.getNome() == Tag.OP_SUBTRACTION:
                self.sinalizaErroSintatico(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=, +, -", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Exp3)
            else:
                self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=, +, -", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Exp3()
                    
    def Exp3Line(self):
        if self.eat(Tag.OP_MULTIPLICATION):
            self.Exp4()
            self.Exp3Line()
        elif self.eat(Tag.OP_DIVISION):
            self.Exp4()
            self.Exp3Line()
        # skip: (Exp3Line)
        else:
            self.skip(f'Esperado "*, /", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Exp3Line()
                
    def Exp4(self):
        if self.eat(Tag.ID):
            self.Exp4Line()
        elif not self.eat(Tag.INTEGER) or not self.eat(Tag.DOUBLE) or not self.eat(Tag.STRING) or not self.eat(Tag.KW_TRUE) or not self.eat(Tag.KW_FALSE):
            self.sinalizaErroSintatico(f'Esperado "CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE", encontrado "{self.token.getLexema()}"')
        elif self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION:
            self.OpUnario()
            self.Exp4()
        elif self.eat(Tag.CHAR_OPEN_PARENTHESES):
            self.Expressao()
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Esperado ")", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(Exp4)
            if self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT or self.token.getNome() == Tag.OP_SUM or self.token.getNome() == Tag.OP_SUBTRACTION or self.token.getNome() == Tag.OP_MULTIPLICATION or self.token.getNome() == Tag.OP_DIVISION:
                self.sinalizaErroSintatico(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=, +, -, *, /", encontrado "{self.token.getLexema()}"')
                return
            # skip: (Exp4)
            else:
                self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=, +, -, *, /", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Exp4()
                    
    def Exp4Line(self):
        if self.eat(Tag.CHAR_OPEN_PARENTHESES):
            self.RegexExp()
            if self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Esperado ")", encontrado "{self.token.getLexema()}"')
        # skip: (Exp4Line)
        else:
            self.skip(f'Esperado "(", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Exp4Line()
                
    def OpUnario(self):
        if not self.eat(Tag.OP_NEGATION) or not self.eat(Tag.OP_EXCLAMATION):
            self.sinalizaErroSintatico(f'Esperado "-, !", encontrado "{self.token.getLexema()}"')
        else:
            # synch: FOLLOW(OpUnario)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE:
                self.sinalizaErroSintatico(f'Esperado "-, !, ID, (, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE", encontrado "{self.token.getLexema()}"')
                return
            # skip: (OpUnario)
            else:
                self.skip(f'Esperado "-, !, ID, (, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.OpUnario()
