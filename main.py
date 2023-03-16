#!/usr/bin/python

import os, pprint
from encoder import GolombRice

def load(datapath: str, debug=False) -> list[str]:
    '''
    Retuns a list of all filename included in corpus sylesia
    '''
    files = [datapath + f for f in os.listdir(datapath)]
    if debug:
        pprint.pprint(files)
    return files

    
def main():
    files = load('data/', debug=True)

    gr = GolombRice()
    
    
if __name__ == '__main__':
    main()
