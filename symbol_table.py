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
                return '<' + create_kw + ', ' + self.dict_symbol[create_kw]
            elif create_op in self.dict_symbol:
                return '<' + create_op + ', ' + self.dict_symbol[create_op]
            elif create_id in self.dict_symbol:
                return '<' + create_id + ', ' + self.dict_symbol[create_id]
            else:
                self.dict_symbol[create_id] = lexema
                return '<' + create_id + ', ' + self.dict_symbol[create_id]

        except Exception as err:
            print(f'{err}')
