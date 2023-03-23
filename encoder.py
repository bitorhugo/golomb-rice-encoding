import math

class GolombRice():

    def __init__(self, file: str, debug: bool=False) -> None:
        '''
        '''
        self.byte_seq, self.bits_seq = self.__byte_seq(file, debug)

        
    def __byte_seq(self, file: str, debug: bool=False) -> tuple[list[int], list[int]]:
        seq = []
        seq_bits = []
        with open(file, 'rb') as f:
            b = f.read(1)
            i = 0
            while(b):
                byte = ord(b)
                seq.append(byte)
                bits = bin(byte)[2:].rjust(8, '0') # rjust will pad 0's to the left
                seq_bits.append(bits)
                if debug:
                    print(f'byte: {byte}')
                    print(f'bits: {bits}')
                    print('-------------')
                    i += 1
                    if i == 200:
                        break
                b = f.read(1)
        return (seq, seq_bits)
            

    def encode(self):
        '''
        '''
        pass


    def decode(self):
        '''
        '''
        pass


    def q(self, n: int, m: float) -> int:
        '''
        Calculates quoficient and returns it as unary
        q = n / m, rounded to the floor
        '''
        q = math.floor( n/m )
        value = ''
        for _ in range(q):
            value += '1'
        value += '0'
        return int(value)

    
    def m(self) -> float:
        '''
        m is a formula that will be rounded to the nearest base 2 exponential value
        m = -log(1+zero_prob)/log(zero_prob)
        '''
        zero_prob = self.zero_prob()
        return self.__next_power_of_two(-(math.log(1 + zero_prob) / math.log(zero_prob)))

    
    def __next_power_of_two(self, x: float) -> int:
        return 1 if x == 0 else 2**math.ceil(math.log2(x))

    
    def zero_prob(self, debug: bool=False) -> float:
        count = 0
        for byte in self.byte_seq:
            bits = bin(byte)[2:].rjust(8, '0')
            count += bits.count('0')
        if debug:
            print(f'zero_count: {count}')
            print(f'total_bits: {len(self.byte_seq) * 8}')
            print(f'prob: {count/(len(self.byte_seq) * 8)}')
        return count/(len(self.byte_seq) * 8)
