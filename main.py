from automaton import Automaton
import os

def reader_file(filepath):
    with open(filepath) as f:
        eof = False
        return_pointer = False
        automaton = Automaton()
        print("\n=>Lista de tokens:")

        while eof is False:
            char = f.read(1)
            
            content, return_pointer = automaton.verify_lexema(char)

            if return_pointer:
                f.seek(f.tell()-1, os.SEEK_SET)
            if content != None:
                print(content)
            if not char:
                eof = True

        print("\n=>Tabela de simbolos:")

        automaton.print_symbol_table()
        
        try:
            f.close()
        except IOError:
            print('Erro ao fechar arquivo. Encerrando.')
            sys.exit(0)
            
        print('\n=> Fim da compilacao')

if __name__ == '__main__':
    reader_file('./files/teste.txt')