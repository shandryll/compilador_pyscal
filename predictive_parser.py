import sys

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo

    def sinalizaErroSintatico(self, message):
        print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
        print(message, "\n")

    def advance(self):
        print("[DEBUG] token: ", self.token.toString())
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
        if(self.token.getNome() != "EOF"):
            self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def Classe(self):
        # Classe -> "class" ID ":" ListaFuncao  Main "end" "."
        if self.eat("KW_CLASS"): 
            if not self.eat("ID"):
                self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\"")
            if not self.eat("CHAR_TWO_POINTS"):
                self.sinalizaErroSintatico("Esperado \":\", encontrado " + "\"" + self.token.getLexema() + "\"")

            self.ListaFuncao()
            self.Main()

            if not self.eat("KW_END") :
                self.sinalizaErroSintatico("Esperado \"end\", encontrado " + "\"" + self.token.getLexema() + "\"")
            if not self.eat("CHAR_POINT"):
                self.sinalizaErroSintatico("Esperado \".\", encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            