import sys
from tag import Tag
from symbol_table import SymbolTable
from token import Token
from no import No

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
        self.cont_erros = 0
        self.symbol_table = SymbolTable()

    def sinalizaErroSintatico(self, message):
        print("\n")
        print(f'[Erro Sintatico] na linha "{str(self.token.getLinha())}" e coluna "{str(self.token.getColuna())}":')
        print(message, "\n")
        self.cont_erros = self.cont_erros + 1
        if self.cont_erros >= 5:
            sys.exit(0)

    def sinalizaErroSemantico(self, message):
        print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
        print(message, "\n")
        self.cont_erros = self.cont_erros + 1
        if self.cont_erros >= 5:
            sys.exit(0)

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
            tempTok = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            else:
                self.symbol_table.setTipo(tempTok.getLexema(), Tag.VAZIO)

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
                self.skip(f'Esperado "CLASS, EOF", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    self.Classe()

    def DeclaraID(self):
        if self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID:
            noTipoPrimitivo = self.TipoPrimitivo()

            tempTok = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            else:
                self.symbol_table.setTipo(tempTok.getLexema(), noTipoPrimitivo.getTipo())
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
        # ListaFuncao -> epsilon
        elif self.token.getNome() == Tag.KW_DEFSTATIC:
            return
        # skip: (ListaFuncao)
        else:
            self.skip(f'Esperado "DEF", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaFuncao()

    def ListaFuncaoLine(self):
        # ListaFuncaoLine -> Funcao ListaFuncao'
        if self.token.getNome() == Tag.KW_DEF:
            self.Funcao()
            self.ListaFuncaoLine
        # ListaFuncao -> epsilon
        elif self.token.getNome() == Tag.KW_DEFSTATIC:
            return
        # skip: (ListaFuncaoLine)
        else:
            self.skip(f'Esperado "DEF", "DEFSTATIC", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaFuncaoLine()
    
    def Funcao(self):
        if self.eat(Tag.KW_DEF): 
            noTipoPrimitivo = self.TipoPrimitivo()

            tempTok = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            else:
                self.symbol_table.setTipo(tempTok.getLexema(), noTipoPrimitivo.getTipo())
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')

            self.ListaArg()

            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_TWO_POINTS):
                self.sinalizaErroSintatico(f'Era esperado ":", encontrado "{self.token.getLexema()}"')

            self.RegexDeclaraID()
            self.ListaCmd()
            noRetorno = self.Retorno()

            if(noRetorno.getTipo() != noTipoPrimitivo.getTipo()):
                self.sinalizaErroSemantico("Tipo de retorno incompativel")

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
        # RegexDeclaraID -> episilon
        elif self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
            return
        # skip: (RegexDeclaraID)
        else:
            self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID, END, RETURN, IF, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
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
        # ListaArgLine -> episilon
        elif self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES:
            return
        # skip: (ListaArgLine)
        else:
            self.skip(f'Esperado ",, )", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaArgLine()
                
    def Arg(self):
        if self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID:
            noTipoPrimitivo = self.TipoPrimitivo()

            tempTok = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico(f'Era esperado "ID", encontrado "{self.token.getLexema()}"')
            else:
                self.symbol_table.setTipo(tempTok.getLexema(), noTipoPrimitivo.getTipo())
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
        noRetorno = No()

        if self.eat(Tag.KW_RETURN):
            noExpressao = self.Expressao()
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado "RETURN, ;", encontrado "{self.token.getLexema()}"')
            else:
                noRetorno.setTipo(noExpressao.getTipo)
                return noRetorno
        elif self.token.getNome() == Tag.KW_END:
            noRetorno.setTipo(Tag.VAZIO)
            return noRetorno
        # skip: (Retorno)
        else:
            self.skip(f'Esperado "RETURN, ;", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                return self.Retorno()
    
    def Main(self):
        if self.eat(Tag.KW_DEFSTATIC):

            tempTok = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

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
            else:
                self.symbol_table.setTipo(tempTok.getLexema(), Tag.TEXTO)
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
        noTipoPrimitivo = No()

        if self.eat(Tag.KW_BOOL):
            noTipoPrimitivo.setTipo(Tag.LOGICO)
            return noTipoPrimitivo
        elif self.eat(Tag.KW_INTEGER):
            noTipoPrimitivo.setTipo(Tag.NUMERICO)
            return noTipoPrimitivo
        elif self.eat(Tag.KW_STRING):
            noTipoPrimitivo.setTipo(Tag.TEXTO)
            return noTipoPrimitivo
        elif self.eat(Tag.KW_DOUBLE):
            noTipoPrimitivo.setTipo(Tag.NUMERICO)
            return noTipoPrimitivo
        elif self.eat(Tag.KW_VOID):
            noTipoPrimitivo.setTipo(Tag.VAZIO)
            return noTipoPrimitivo
        else:
            # synch: FOLLOW(TipoPrimitivo)
            if self.token.getNome() == Tag.ID:
                self.sinalizaErroSintatico(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID", encontrado "{self.token.getLexema()}"')
                return noTipoPrimitivo
            # skip: (TipoPrimitivo)
            else:
                self.skip(f'Esperado "BOOL, INTEGER, STRING, DOUBLE, VOID, ID", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    return self.TipoPrimitivo()
                    
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
        # ListaCmdLine -> episilon
        elif self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_ELSE:
            return
        # skip: (ListaCmdLine)
        else:
            self.skip(f'Esperado "IF, WHILE, ID, WRITE, END, RETURN, ELSE", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.ListaCmdLine()
                
    def Cmd(self):
        tempTok = Token(self.token.getNome(), self.token.getLexema(), self.token.getLinha(), self.token.getColuna())

        if self.token.getNome() == Tag.KW_IF:
            self.CmdIf()
        elif self.token.getNome() == Tag.KW_WHILE:
            self.CmdWhile()
        elif self.eat(Tag.ID):
            if tempTok.getLexema() == None:
                self.sinalizaErroSemantico("ID " + tempTok.getLexema() + " não declarado")
            noCmdAtribFunc = self.CmdAtribFunc()
            if noCmdAtribFunc.getTipo() != Tag.VAZIO and self.symbol_table.getTipo(tempTok.getLexema()) != noCmdAtribFunc.getTipo():
                self.sinalizaErroSemantico("atribuição incompatível")
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
        noCmdAtribFunc = No()

        if self.token.getNome() == Tag.OP_ASSIGN:
            noCmdAtribui = self.CmdAtribui()
            noCmdAtribFunc.setTipo(noCmdAtribui.getTipo())
            return noCmdAtribFunc
        elif self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            self.CmdFuncao()
            noCmdAtribFunc.setTipo(Tag.VAZIO)
            return noCmdAtribFunc
        else:
            # synch: FOLLOW(CmdAtribFunc)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "=, (, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return noCmdAtribFunc
            # skip: (CmdAtribFunc)
            else:
                self.skip(f'Esperado "=, (, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    return self.CmdAtribFunc()
                    
    def CmdIf(self):
        if self.eat(Tag.KW_IF):
            if not self.eat(Tag.CHAR_OPEN_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado "(", encontrado "{self.token.getLexema()}"')    
            
            noExpressao = self.Expressao()
            
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')  
            else:
                if noExpressao.getTipo() != Tag.LOGICO:
                    self.sinalizaErroSemantico("A condição não resulta em um valor logico")    
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
            
            noExpressao = self.Expressao()    
              
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            else:
                if noExpressao.getTipo() != Tag.LOGICO:
                    self.sinalizaErroSemantico("A condição não resulta em um valor logico")
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
            
            noExpressao = self.Expressao()    
              
            if not self.eat(Tag.CHAR_CLOSE_PARENTHESES):
                self.sinalizaErroSintatico(f'Era esperado ")", encontrado "{self.token.getLexema()}"')
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
            else:
                if noExpressao.getTipo() != Tag.TEXTO:
                    self.sinalizaErroSemantico("O conteudo não é um TEXTO")
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
        noCmdAtribui = No()

        if self.eat(Tag.OP_ASSIGN):
            noExpressao = self.Expressao()
            
            if not self.eat(Tag.CHAR_SEMICOLON):
                self.sinalizaErroSintatico(f'Era esperado ";", encontrado "{self.token.getLexema()}"')
            else:
                noCmdAtribui.setTipo(noExpressao.getTipo())
                return noCmdAtribui
        else:
            # synch: FOLLOW(CmdAtribui)
            if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_END or self.token.getNome() == Tag.KW_RETURN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_ELSE or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.KW_WRITE:
                self.sinalizaErroSintatico(f'Esperado "=, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                return noCmdAtribui
            # skip: (CmdAtribui)
            else:
                self.skip(f'Esperado "=, ID, END, RETURN, IF, ELSE, WHILE, WRITE", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    return self.CmdAtribui()
                    
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
        # RegexExp -> episilon
        elif self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES:
            return
        # skip: (RegexExp)
        else:
            self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, )", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.RegexExp()
                
    def RegexExpLine(self):
        if self.eat(Tag.CHAR_COMMA):
            self.Expressao()
            self.RegexExpLine()
        # RegexExpLine -> episilon
        elif self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES:
            return
        # skip: (RegexExpLine)
        else:
            self.skip(f'Esperado ",, )", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.RegexExpLine()
    
    def Expressao(self):
        noExpressao = No()

        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            noExp1 = self.Exp1()
            noExpLine = self.ExpLine()

            if noExpLine.getTipo() == Tag.VAZIO:
                noExpressao.setTipo(noExp1.getTipo())
            elif noExpLine.getTipo() == noExp1.getTipo() and noExpLine.getTipo() == Tag.LOGICO:
                noExpressao.setTipo(Tag.LOGICO)
            else:
                noExpressao.setTipo(Tag.ERRO)

            return noExpressao
        # skip: (Expressao)
        else:
            self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                return self.Expressao()
                
    def ExpLine(self):
        noExpLine = No()

        if self.eat(Tag.OP_OR):
            noExp1 = self.Exp1()
            noExpLineFilho = self.ExpLine()

            if noExpLineFilho.getTipo() == Tag.VAZIO:
                noExpLine.setTipo(noExp1.getTipo())
            elif noExpLineFilho.getTipo() == noExp1.getTipo() and noExpLineFilho.getTipo() == Tag.LOGICO:
                noExpLine.setTipo(Tag.LOGICO)
            else:
                noExpLine.setTipo(Tag.ERRO)

            return noExpLine

        elif self.eat(Tag.OP_AND):
            noExp1 = self.Exp1()
            noExpLine = self.ExpLine()

            if noExpLineFilho.getTipo() == Tag.VAZIO:
                noExpLine.setTipo(noExp1.getTipo())
            elif noExpLineFilho.getTipo() == noExp1.getTipo() and noExpLineFilho.getTipo() == Tag.LOGICO:
                noExpLine.setTipo(Tag.LOGICO)
            else:
                noExpLine.setTipo(Tag.ERRO)

            return noExpLine
        # ExpLine -> episilon
        elif self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA:
            noExpLine.setTipo(Tag.VAZIO)
            return noExpLine
        # skip: (ExpLine)
        else:
            self.skip(f'Esperado "OR, AND, ;, ), ,", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                return self.ExpLine()
                
    def Exp1(self):
        noExp1 = No()

        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            noExp2 = self.Exp2()
            noExp1Line = self.Exp1Line()

            if noExp1Line.getTipo() == Tag.VAZIO:
                noExp1.setTipo(noExp2.getTipo())
            elif noExp1Line.getTipo() == noExp2.getTipo() and noExp1Line.getTipo() == Tag.NUMERICO:
                noExp1.setTipo(Tag.LOGICO)
            else:
                noExp1.setTipo(Tag.ERRO)

            return noExp1
        else:
        # synch: FOLLOW(Exp1)
            if self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND:
                self.sinalizaErroSintatico(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and", encontrado "{self.token.getLexema()}"')
                return noExp1
            # skip: (Exp1)
            else:
                self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    return self.Exp1()
                    
    def Exp1Line(self):
        noExp1Line = No()

        if self.eat(Tag.OP_LESS):
            noExp2 = self.Exp2()
            noExp1LineFilho = self.Exp1Line()

            if noExp1LineFilho.getTipo() == Tag.VAZIO and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            elif noExp1LineFilho.getTipo() == noExp2.getTipo() and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            else:
                noExp1Line.setTipo(Tag.ERRO)

            return noExp1Line
        elif self.eat(Tag.OP_LESS_EQUAL):
            self.Exp2()
            self.Exp1Line()

            if noExp1LineFilho.getTipo() == Tag.VAZIO and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            elif noExp1LineFilho.getTipo() == noExp2.getTipo() and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            else:
                noExp1Line.setTipo(Tag.ERRO)

            return noExp1Line
        elif self.eat(Tag.OP_GREATER):
            self.Exp2()
            self.Exp1Line()

            if noExp1LineFilho.getTipo() == Tag.VAZIO and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            elif noExp1LineFilho.getTipo() == noExp2.getTipo() and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            else:
                noExp1Line.setTipo(Tag.ERRO)

            return noExp1Line
        elif self.eat(Tag.OP_GREATER_EQUAL):
            self.Exp2()
            self.Exp1Line()

            if noExp1LineFilho.getTipo() == Tag.VAZIO and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            elif noExp1LineFilho.getTipo() == noExp2.getTipo() and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            else:
                noExp1Line.setTipo(Tag.ERRO)

            return noExp1Line
        elif self.eat(Tag.OP_EQUAL):
            self.Exp2()
            self.Exp1Line()

            if noExp1LineFilho.getTipo() == Tag.VAZIO and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            elif noExp1LineFilho.getTipo() == noExp2.getTipo() and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            else:
                noExp1Line.setTipo(Tag.ERRO)

            return noExp1Line
        elif self.eat(Tag.OP_DIFFERENT):
            self.Exp2()
            self.Exp1Line()

            if noExp1LineFilho.getTipo() == Tag.VAZIO and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            elif noExp1LineFilho.getTipo() == noExp2.getTipo() and noExp2.getTipo() == Tag.NUMERICO:
                noExp1Line.setTipo(Tag.NUMERICO)
            else:
                noExp1Line.setTipo(Tag.ERRO)

            return noExp1Line
        elif self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND:
            noExp1Line.setTipo(Tag.VAZIO)
            return noExp1Line
        # skip: (Exp1Line)
        else:
            self.skip(f'Esperado "<, <=, >, >=, ==, !=, ;, ), ,, OR, AND", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                return self.Exp1Line()
                
    def Exp2(self):
        noExp2 = No()

        if self.token.getNome() == Tag.ID or self.token.getNome() == Tag.INTEGER or self.token.getNome() == Tag.DOUBLE or self.token.getNome() == Tag.STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_NEGATION or self.token.getNome() == Tag.OP_EXCLAMATION or self.token.getNome() == Tag.CHAR_OPEN_PARENTHESES:
            noExp3 = self.Exp3()
            noExp2Line = self.Exp2Line()

            if noExp2Line.getTipo() == Tag.VAZIO:
                noExp2.setTipo(noExp3.getTipo())
            elif noExp2Line.getTipo() == noExp3.getTipo() and noExp2Line.getTipo() == Tag.NUMERICO:
                noExp2.setTipo(Tag.NUMERICO)
            else:
                noExp2.setTipo(Tag.ERRO)

            return noExp2
        else:
        # synch: FOLLOW(Exp2)
            if self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT:
                self.sinalizaErroSintatico(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=", encontrado "{self.token.getLexema()}"')
                return noExp2
            # skip: (Exp2)
            else:
                self.skip(f'Esperado "ID, CONST_INTEGER, CONST_DOUBLE, CONST_STRING, TRUE, FALSE, -, !, (, ;, ), ,, or, and, <, <=, >, >=, ==, !=", encontrado "{self.token.getLexema()}"')
                if(self.token.getNome() != Tag.EOF): 
                    return self.Exp2()
                    
    def Exp2Line(self):
        if self.eat(Tag.OP_SUM):
            self.Exp3()
            self.Exp2Line()
        elif self.eat(Tag.OP_SUBTRACTION):
            self.Exp3()
            self.Exp2Line()
        elif self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT:
            return
        # skip: (Exp2Line)
        else:
            self.skip(f'Esperado "+, -, ;, ), ,, OR, AND, <, <=, >, >=, ==, !=", encontrado "{self.token.getLexema()}"')
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
        elif self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT or self.token.getNome() == Tag.OP_SUM or self.token.getNome() == Tag.OP_SUBTRACTION:
            return
        # skip: (Exp3Line)
        else:
            self.skip(f'Esperado "*, /, ;, ), ,, OR, AND, <, <=, >, >=, ==, !=, +, -", encontrado "{self.token.getLexema()}"')
            if(self.token.getNome() != Tag.EOF): 
                self.Exp3Line()
                
    def Exp4(self):
        if self.eat(Tag.ID):
            self.Exp4Line()
        elif self.eat(Tag.INTEGER) or self.eat(Tag.DOUBLE) or self.eat(Tag.STRING) or self.eat(Tag.KW_TRUE) or self.eat(Tag.KW_FALSE):
            return
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
        elif self.token.getNome() == Tag.CHAR_SEMICOLON or self.token.getNome() == Tag.CHAR_CLOSE_PARENTHESES or self.token.getNome() == Tag.CHAR_COMMA or self.token.getNome() == Tag.OP_OR or self.token.getNome() == Tag.OP_AND or self.token.getNome() == Tag.OP_LESS or self.token.getNome() == Tag.OP_LESS_EQUAL or self.token.getNome() == Tag.OP_GREATER or self.token.getNome() == Tag.OP_GREATER_EQUAL or self.token.getNome() == Tag.OP_EQUAL or self.token.getNome() == Tag.OP_DIFFERENT or self.token.getNome() == Tag.OP_SUM or self.token.getNome() == Tag.OP_SUBTRACTION or self.token.getNome() == Tag.OP_MULTIPLICATION or self.token.getNome() == Tag.OP_DIVISION:
            return
        # skip: (Exp4Line)
        else:
            self.skip(f'Esperado "(, ;, ), ,, OR, AND, <, <=, >, >=, ==, !=, +, -, *, /", encontrado "{self.token.getLexema()}"')
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
