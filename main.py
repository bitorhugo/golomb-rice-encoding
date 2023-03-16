#!/usr/bin/python

import os, pprint

def main():
    files = [] # corpus sylesia file list
    for root, _, files in os.walk('data'):
        files.append(os.path.join(root))
    files.pop() # remove hanging dir name
    pprint.pprint(files)

if __name__ == '__main__':
    main()
