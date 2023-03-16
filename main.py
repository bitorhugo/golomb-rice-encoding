#!/usr/bin/python

import os, pprint
from encoder import GolombRice

def load(datapath: str, debug=False) -> dict[str, list[str]]:
    '''
    Retuns a list of all filename included in corpus sylesia
    '''
    dirs = []
    files = {}

    dirs = os.listdir(datapath)
    for dir in dirs:
        files[dir] = os.listdir(datapath + dir)

    if debug:
        pprint.pprint(files)

    return files

    
def main():
    files = load('data/', debug=True)
    
    gr = GolombRice()
    
    
if __name__ == '__main__':
    main()
