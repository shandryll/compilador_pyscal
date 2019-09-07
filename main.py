from automaton import Automaton


def reader_file(filepath):
    with open(filepath) as f:

        eof = False
        automaton = Automaton()
        while eof is False:
            char = f.read(1)

            eof = automaton.verify_automaton(char)


if __name__ == '__main__':
    reader_file('./files/teste.txt')
