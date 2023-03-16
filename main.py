#!/usr/bin/python

import os, pprint

def load(datapath: str) -> list[str]:
    '''
    Retuns a list of all filename included in corpus sylesia
    '''
    return [datapath + f for f in os.listdir(datapath)]

    
def main():
    files = load('data/')
    print(files)


    
if __name__ == '__main__':
    main()
