def symbol_table():
    dict_token = {}

    dict_token['KW_CLASS'] = 'class'
    dict_token['KW_END'] = 'end'
    dict_token['KW_DEF'] = 'def'
    dict_token['KW_RETURN'] = 'return'
    dict_token['KW_DEFSTATIC'] = 'defstatic'
    dict_token['KW_MAIN'] = 'main'
    dict_token['KW_VOID'] = 'void'
    dict_token['KW_STRING'] = 'String'
    dict_token['KW_BOOL'] = 'bool'
    dict_token['KW_INTEGER'] = 'integer'
    dict_token['KW_DOUBLE'] = 'double'
    dict_token['KW_IF'] = 'if'
    dict_token['KW_ELSE'] = 'else'
    dict_token['KW_WHILE'] = 'while'
    dict_token['KW_WRITE'] = 'write'
    dict_token['KW_TRUE'] = 'true'
    dict_token['KW_FALSE'] = 'false'
    dict_token['OP_OR'] = 'or'
    dict_token['OP_AND'] = 'and'

    lexema = 'teste'

    create_id = 'ID_' + lexema.upper()

    if create_id not in dict_token:
        dict_token[create_id] = lexema
    else:
        print('erro')

    print()
    print(dict_token)

    for lexema in dict_token:
        print(lexema)

def reader_file():
    with open(f'./files/teste.txt', encoding='utf-8') as f:

        lexema = []

        while True:
            c = f.read(1)

            if not c:
                print
                "End of file"
                break
            elif c == " ":
                print(lexema)
                x = "".join(lexema)
                print(x)
                lexema = []
            else:
                lexema.append(c)

            print
            "Read a character:", c

if __name__ == '__main__':
    # symbol_table()
    reader_file()
