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
        files[dir] = ['data/' + dir + "/" + f for f in os.listdir(datapath + dir)]

    if debug:
        pprint.pprint(files)
    return files

    
def main():
    files = load('data/', debug=True)

    images = files['pic']
    img = images.pop()

    with open(img, 'rb') as f:
        b = f.read(1)
        i = 0
        while(b):
            print(f'byte: {b}')
            print(f'from_int: {int.from_bytes(b, "big")}')
            b = f.read(1)
            if i == 50:
                break
            i += 1

            
if __name__ == '__main__':
    main()
