class SymbolTable:

    def __init__(self):

        self.dict_token = {}

        self.dict_token['KW_CLASS'] = 'class'
        self.dict_token['KW_END'] = 'end'
        self.dict_token['KW_DEF'] = 'def'
        self.dict_token['KW_RETURN'] = 'return'
        self.dict_token['KW_DEFSTATIC'] = 'defstatic'
        self.dict_token['KW_MAIN'] = 'main'
        self.dict_token['KW_VOID'] = 'void'
        self.dict_token['KW_STRING'] = 'String'
        self.dict_token['KW_BOOL'] = 'bool'
        self.dict_token['KW_INTEGER'] = 'integer'
        self.dict_token['KW_DOUBLE'] = 'double'
        self.dict_token['KW_IF'] = 'if'
        self.dict_token['KW_ELSE'] = 'else'
        self.dict_token['KW_WHILE'] = 'while'
        self.dict_token['KW_WRITE'] = 'write'
        self.dict_token['KW_TRUE'] = 'true'
        self.dict_token['KW_FALSE'] = 'false'
        self.dict_token['OP_OR'] = 'or'
        self.dict_token['OP_AND'] = 'and'

    def add_lexema(self, lexema):

        create_kw = 'KW_' + lexema.upper()
        create_op = 'OP_' + lexema.upper()
        create_id = 'ID_' + lexema.upper()

        if create_kw in self.dict_token:
            return '<' + create_kw + ', ' + self.dict_token[create_kw] + '>'
        elif create_op in self.dict_token:
            return self.dict_token[create_op]
        elif create_id in self.dict_token:
            return self.dict_token[create_id]
        else:
            self.dict_token[create_id] = lexema
            return '<' + create_id + ', ' + self.dict_token[create_id] + '>'