from token import Token
from tag import Tag

class SymbolTable:

    def __init__(self):
        self.dict_symbol = {}
        self.dict_symbol['class'] = Token(Tag.KW_CLASS, 'class', 0, 0)
        self.dict_symbol['end'] = Token(Tag.KW_END, 'end', 0, 0)
        self.dict_symbol['def'] = Token(Tag.KW_DEF, 'def', 0, 0)
        self.dict_symbol['return'] = Token(Tag.KW_RETURN, 'return', 0, 0)
        self.dict_symbol['defstatic'] = Token(Tag.KW_DEFSTATIC, 'defstatic', 0, 0)
        self.dict_symbol['main'] = Token(Tag.KW_MAIN, 'main', 0, 0)
        self.dict_symbol['void'] = Token(Tag.KW_VOID, 'void', 0, 0)
        self.dict_symbol['String'] = Token(Tag.KW_STRING, 'String', 0, 0)
        self.dict_symbol['bool'] = Token(Tag.KW_BOOL, 'bool', 0, 0)
        self.dict_symbol['integer'] = Token(Tag.KW_INTEGER, 'integer', 0, 0)
        self.dict_symbol['double'] = Token(Tag.KW_DOUBLE, 'double', 0, 0)
        self.dict_symbol['if'] = Token(Tag.KW_IF, 'if', 0, 0)
        self.dict_symbol['else'] = Token(Tag.KW_ELSE, 'else', 0, 0)
        self.dict_symbol['while'] = Token(Tag.KW_WHILE, 'while', 0, 0)
        self.dict_symbol['write'] = Token(Tag.KW_WRITE, 'write', 0, 0)
        self.dict_symbol['true'] = Token(Tag.KW_TRUE, 'true', 0, 0)
        self.dict_symbol['false'] = Token(Tag.KW_FALSE, 'false', 0, 0)
        self.dict_symbol['or'] = Token(Tag.OP_OR, 'or', 0, 0)
        self.dict_symbol['and'] = Token(Tag.OP_AND, 'and', 0, 0)
        

    def getToken(self, lexema):
        token = self.dict_symbol.get(lexema)
        return token

    def addToken(self, lexema, token):
        self.dict_symbol[lexema] = token

    def print_symbol_table(self):
        for k, t in (self.dict_symbol.items()):
            print(k, ":", t.toString())