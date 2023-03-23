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
            byte = ord(b)
            bits = bin(byte)[2:].rjust(8, '0') # rjust will pad 0's to the left
            int_value = ord(b)
            print(f'byte: {byte}')
            print(f'bits: {bits}')
            print(f'int: {int_value}')
            print('-------------')
            b = f.read(1)
            if i == 20:
                break
            i += 1

            
if __name__ == '__main__':
    main()
