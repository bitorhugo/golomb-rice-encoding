#!/usr/bin/python3

import os, pprint
import cProfile, re
import tkinter
from tkinter import Button, Label, Tk, filedialog
from golombrice import GolombRice


# def load(datapath: str, debug=False) -> dict[str, list[str]]:
#     '''
#     Retuns a list of all filename included in corpus sylesia
#     '''
#     files = {}
#     dirs = os.listdir(datapath)
#     for dir in dirs:
#         files[dir] = ['data/corpus-silesia/' + dir + "/" + f for f in os.listdir(datapath + dir)]
#     if debug:
#         pprint.pprint(files)
#     return files

def extract():
    f = filedialog.askopenfilename(initialdir = "~/", title = "Select a File to extract")
    print(f'File Selected: {f}')
    gr = GolombRice()
    gr.decode(f)
    print(f'Extraction DONE')

    
def compress():
    f = filedialog.askopenfilename(initialdir = "~/", title = "Select a File to compress")
    print(f'File Selected: {f}')
    gr = GolombRice()
    gr.encode(file=f)
    print(f'Compression DONE')


def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "~/projects", title = "Select a File")
    print(f'File Selected: {filename}')
    return filename


def gui() -> None:
    window = Tk()
    window.title('File Explorer')
    window.geometry("500x500")
    window.config(background = "white")
    label_file_explorer = Label(window, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
    button_compress = Button(window,
                             text = "Compress",
                             command = compress)
    button_extract = Button(window,
                             text = "Extract",
                             command = extract)
    button_exit = Button(window,
                     text = "Exit",
                     command = exit)
    label_file_explorer.grid(column = 0, row = 1)
    button_compress.grid(column = 0, row = 2)
    button_extract.grid(column = 0, row = 3)
    button_exit.grid(column = 0, row = 4)
    window.mainloop()    

    
def main():
    gui()
    
    # files = load('data/corpus-silesia/', debug=True)
    # directory = files['exe']
    # f = directory[0]

    # debug = True
    # gr = GolombRice()
    
    # enc = gr.encode(file=f, debug=debug)
    # gr.decode(enc, debug=debug)


if __name__ == '__main__':
    # cProfile.run('main()')
    main()


    
# distribuicao geometrica (probabilidade de simbolos com menor valr inteiro e maior)
