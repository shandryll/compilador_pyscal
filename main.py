from SymbolTable import SymbolTable

def reader_file():
    with open(f'./files/teste.txt', encoding='utf-8') as f:

        symbol_table = SymbolTable()

        lexema = ""

        while True:
            c = f.read(1)

            if not c:
                print(symbol_table.add_lexema(lexema))
                break
            elif c == " ":
                print(symbol_table.add_lexema(lexema))
                lexema = ""
            else:
                lexema = lexema + c

if __name__ == '__main__':
    # symbol_table()
    reader_file()
