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

    gr = GolombRice(img, debug=True)
    print (f'zero_prob: {gr.zero_prob()}')
if __name__ == '__main__':
    main()
