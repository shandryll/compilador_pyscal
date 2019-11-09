from predictive_parser import Parser
from automaton import Automaton
import os, sys

def reader_file(filepath):

    lexer = Automaton(filepath)
    parser = Parser(lexer)

    parser.Programa()
    parser.lexer.closeFile()

    print("\n=> Tabela de símbolos:")
    lexer.print_symbol_table()
        
    print('\n=> Fim da compilação')

if __name__ == '__main__':
    reader_file('./files/HelloPyscal.pys')
