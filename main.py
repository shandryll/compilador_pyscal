from automaton import Automaton
import os

def reader_file(filepath):
    with open(filepath) as f:
        eof = False
        return_pointer = False
        automaton = Automaton()

        while eof is False:
            char = f.read(1)
            
            content, return_pointer = automaton.verify_lexema(char)

            if return_pointer:
                f.seek(f.tell()-1, os.SEEK_SET)
            if content != None:
                print(content)
            if not char:
                eof = True


if __name__ == '__main__':
    reader_file('./files/teste.txt')