from symbol_table import SymbolTable


def reader_file(filepath):
    with open(filepath) as f:

        symbol_table = SymbolTable()

        lexema = ""
        current_line = 1
        current_column = 1

        while True:
            char = f.read(1)

            if not char == '\n':
                if not char:
                    print(symbol_table.add_lexema(lexema) + " - line: " + str(current_line) + ", column: " + str(current_column) + '>')
                    break
                elif char == ' ':
                    print(symbol_table.add_lexema(lexema) + " - line: " + str(current_line) + ", column: " + str(current_column) + '>')
                    lexema = ''
                else:
                    lexema = lexema + char

                current_column = current_column + 1

            elif char == '\n':
                print(symbol_table.add_lexema(lexema) + " - line: " + str(current_line) + ", column: " + str(current_column) + '>')
                lexema = ''
                current_column = 1
                current_line = current_line + 1


if __name__ == '__main__':
    reader_file('./files/teste.txt')
