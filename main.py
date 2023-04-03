#!/usr/bin/python

import os, pprint
from encoder import GolombRice

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
    images = files['pic']
    img = images.pop()

    gr = GolombRice(img, debug=True)
    gr.encode(debug=True)

        
if __name__ == '__main__':
    main()



