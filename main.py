#!/usr/bin/python3

import os, pprint
import cProfile, re

import bitstring
from golombrice import GolombRice


def load(datapath: str, debug=False) -> dict[str, list[str]]:
    '''
    Retuns a list of all filename included in corpus sylesia
    '''
    files = {}
    dirs = os.listdir(datapath)
    for dir in dirs:
        files[dir] = ['data/corpus-silesia/' + dir + "/" + f for f in os.listdir(datapath + dir)]
    if debug:
        pprint.pprint(files)
    return files

    
def main():
    files = load('data/corpus-silesia/', debug=True)
    directory = files['pic']
    f = directory.pop()

    debug = False
    gr = GolombRice()
    
    enc = gr.encode(file = f, debug=debug)
    gr.decode(enc, debug=debug)


if __name__ == '__main__':
    # cProfile.run('main()')
    main()





    
# distribuicao geometrica (probabilidade de simbolos com menor valr inteiro e maior)

# 9970564
# 6154730
# 12833709

# 33553454
# 26170561 
# 68299882


