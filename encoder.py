import re

class GolombRice():
    

    def __init__(self, file: str, m: int=16, debug: bool=False) -> None:
        '''
        '''
        self.byte_seq = self.__byte_seq(file, debug)
        self.m = m


    def __byte_seq(self, file: str, debug: bool=False) -> list[int]:
        seq = []
        with open(file, 'rb') as f:
            b = f.read(1)
            i = 0
            while(b):
                byte = ord(b)
                bits = bin(byte)[2:].rjust(8, '0') # rjust will pad 0's to the left
                seq.append(byte)
                i += 1
                if i == 200:
                    break
                if debug:
                    print(f'byte: {byte}')
                    print(f'bits: {bits}')
                    print('-------------')
                b = f.read(1)
        return seq
            
    def encode(self):
        '''
        '''
        pass


    def decode(self):
        '''
        '''
        pass

    def zero_prob(self) -> float:
        for byte in self.byte_seq:
            bits = bin(byte)[2:].rjust(8, '0')
        return 0.0
