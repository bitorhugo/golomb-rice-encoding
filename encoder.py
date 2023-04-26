import math, bitstring, time
from functools import reduce

class GolombRice():

    input_path: str
    encoding_path: str
    decoding_path: str

    c: int
    m: int
    output_buffer: list[str]
    aligned_bits: int

    def __init__(self, input_path :str) -> None:
        self.input_path = input_path
        self.encoding_path = 'data/encodings/test'
        self.decoding_path = 'data/decodings/test'
        self.output_buffer = []
        
    def encode(self, debug: bool=False):
        '''
        Encodes input stream
        '''
        # transform input to bit array
        if debug:
            bitstream = bitstring.BitArray('0b000001001100010100000111010001')
        else:
            bitstream = bitstring.BitArray(filename=self.input_path)

        # represent input as a sequence of zeros
        symbol_buffer, zero_count = self.__symbol_seq(bitstream)

        # start timer
        start = time.time()

        # calculate probability of zeros
        p = self.__p(bitstream, zero_count)
        if debug:
            print(f'p(0): {p}')
        # calculate m
        m = self.__m(p)
        self.m = m
        if debug:
            print (f'm: {m}')

        # calculate c, also named as 'k'
        self.c = self.__c(m)
        if debug:
            print(f'c: {self.c}')

        for symbol in symbol_buffer:
            if debug:
                print(f'symbol: {symbol}')
                
            # compute quotient 'q'
            q_value, q_unary = self.__q(symbol, self.c) # q is a tuple containing its integer value and its unary representation
            if debug:
                print(f'q: {(q_value, q_unary)}')
                
            # compute remainder and represent it in 'c' bits
            r = self.r(symbol, q_value, m, self.c)
            if debug:
                print(f'r: {r}')

            # represent final encoding as a concatenation of 'q' and 'r'
            cod = str(q_unary) + r

            # append to output buffer
            self.output_buffer.append(cod)

        # terminate timer
        end = time.time()
        elapsed = end - start
        print(f'Encoding-Time: ~{int(elapsed)} seconds')

        if debug:
            print(self.output_buffer)

        # write encoded output to file
        with open('data/encodings/test', 'wb+') as f:
            # join output buffer to single string
            bits = ''.join(self.output_buffer)

            # divide string into bytes
            substring_list = [bits[i:i+8] for i in range(0, len(bits), 8)]

            # pad last byte and save number of last aligned bits 
            self.aligned_bits = 8 - len(substring_list[len(substring_list) - 1])
            if len(substring_list[len(substring_list) - 1]) != 8:
                substring_list[len(substring_list) - 1] = substring_list[len(substring_list) - 1].ljust(8, '0')

            if debug:
                print(f'aligned: {self.aligned_bits}')
                print(substring_list)
                
            # transform string to bytes
            bytes_list = [int(i, 2).to_bytes(1, byteorder='big') for i in substring_list]
            if debug:
                print(bytes_list)

            # write to file
            f.writelines(bytes_list)
            



            
    def decode(self, debug=False):
        '''
        Decodes output stream
        '''
        # TODO: on reading bytes from file, eliminate last aligned bits from the sequence
        encodings = []
        # read encodings from file
        with open (self.encoding_path) as f:
            encodings = f.read()

        size = len(encodings)
        start = 0
        symbols = []
        while True:
            index = encodings.find('0', start)

            # 'q' will be the number of ones until a zero is found (unary-code)
            q = index - start
            print(f'q:{q}')

            # 'r' is the next 'c' chars
            r = encodings[index+1 : index+1+self.c]
            print(f'r:{r}')

            index = index + self.c + 1
            print(f'index:{index}')

            start = index
            print(f'start:{start}')

            # compute symbol from q and r
            symbol = int(q) * self.m + int(r)
            
            symbols.append(symbol)
            
            if index >= size:
                print(symbols)
                break;
            
        
            
        
    def __c(self, m: int) -> int:
        '''
        Calculates the amount of bits necessary to represent r
        '''
        return math.ceil(math.log2(m))

        
    def r(self, n: int, q: int, m: int, c: int) -> str:
        '''
        Calculates remainder and returns it in 'c' amount of bits
        '''
        r = n - q * m
        r_bin = bin(r)[2:]
        padding = c - len(r_bin)
        if padding > 0:
            r_bin = r_bin.zfill(c)
            # print (r_bin)

        return r_bin

    
    def __q(self, n: int, c: int) -> tuple[int, str]:
        '''
        Calculates quoficient and returns it as unary
        q = n / m, rounded to the floor
        '''
        q = n >> c
        unary = ''
        for _ in range(q):
            unary += '1'
        unary += '0'
        return (q, unary)


    def __m(self, p: float) -> int:
        '''
        m is a formula that will be rounded to the nearest base 2 exponential value
        m = -log(1+zero_prob)/log(zero_prob)
        '''
        return math.ceil(self.__next_power_of_two(-math.log(1 + p) / math.log(p)))

    
    def __next_power_of_two(self, x: float) -> int:
        '''
        '''
        return 1 if x == 0 else 2**math.ceil(math.log2(x))


    def __p(self, bitstream: bitstring.BitArray, zero_count: int) -> float:
        '''
        '''
        return zero_count / len(bitstream.bin)


    def __symbol_seq(self, bitstream: bitstring.BitArray) -> tuple[list[int], int]:
        '''
        Calculates sequence of zeros 
        '''
        b = bitstream.bin
        buffer = []
        count = 0

        for s in b.split('1'):
            count += len(s) # save zero count for future reference
            buffer.append(len(s))

        return buffer, count



            
# https://bitstring.readthedocs.io/en/stable/slicing.html
# https://michaeldipperstein.github.io/rice.html
