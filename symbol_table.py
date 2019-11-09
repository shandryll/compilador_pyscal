from token import Token

class SymbolTable:

    def __init__(self):
        self.dict_symbol = {'KW_CLASS': 'class', 'KW_END': 'end', 'KW_DEF': 'def', 'KW_RETURN': 'return',
                           'KW_DEFSTATIC': 'defstatic', 'KW_MAIN': 'main', 'KW_VOID': 'void', 'KW_STRING': 'String',
                           'KW_BOOL': 'bool', 'KW_INTEGER': 'integer', 'KW_DOUBLE': 'double', 'KW_IF': 'if',
                           'KW_ELSE': 'else', 'KW_WHILE': 'while', 'KW_WRITE': 'write', 'KW_TRUE': 'true',
                           'KW_FALSE': 'false', 'OP_OR': 'or', 'OP_AND': 'and'}

    def add_lexema(self, lexema):
        try:
            create_kw = 'KW_' + lexema.upper()
            create_op = 'OP_' + lexema.upper()
            create_id = 'ID_' + lexema.upper()

            if create_kw in self.dict_symbol:
                return Token(create_kw, lexema, 0, 0)
            elif create_op in self.dict_symbol:
                return Token(create_op, lexema, 0, 0)
            elif create_id in self.dict_symbol:
                return Token("ID", lexema, 0, 0)
            else:
                self.dict_symbol[create_id] = lexema
                return Token("ID", lexema, 0, 0)

        except Exception as err:
            print(f'{err}')

    def print_symbol_table(self):
        for token_id, token_value in self.dict_symbol.items():
            print(token_id, ":", token_value)