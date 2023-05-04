import math, bitstring, time, struct, os 

class GolombRice():

    input_path: str
    encoding_path: str
    decoding_path: str

    c: int
    m: int

    def __init__(self) -> None:
        pass


    def enc_path(self, filename: str) -> str:
        child: str = filename.split('/').pop()
        return 'data/encodings/' + child + '.enc'


    def dec_path(self, filename: str) -> str:
        child: str = filename.split('/').pop()
        return 'data/decodings/' + child + '.dec'       

    
    def encode(self, file: str, debug: bool=False) -> str:
        '''
        Encodes input stream
        @Param file path of file to encode
        @Param debug debug prints
        @Return file path of encoded file
        '''
        # transform input to bit array
        if debug:
            bitstream = bitstring.BitArray(bin='000001001100010100000111010001')
        else:
            bitstream = bitstring.BitArray(filename=file).bin

        # delcare output buffer
        output_buffer = []
            
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
        if debug:
            print (f'm: {m}')

        # calculate c, also named as 'k'
        c = self.__c(m)
        if debug:
            print(f'c: {c}')

        for symbol in symbol_buffer:
            if debug:
                print(f'symbol: {symbol}')
                
            # compute quotient 'q'
            q_value, q_unary = self.__q(symbol, c) # q is a tuple containing its integer value and its unary representation
            if debug:
                print(f'q: {(q_value, q_unary)}')

            if c > 0:
                # compute remainder and represent it in 'c' bits
                r = self.r(symbol, q_value, m, c)
                if debug:
                    print(f'r: {r}')

                # represent final encoding as a concatenation of 'q' and 'r'
                cod = str(q_unary) + r
            else:
                cod = str(q_unary)

            # append to output buffer
            output_buffer.append(cod)

        # terminate timer
        end = time.time()
        elapsed = end - start
        print(f'Encoding-Time: ~{int(elapsed)} seconds')

        if debug:
            print(output_buffer)

        # write encoded output to file
        enc_path = self.enc_path(file)
        with open(enc_path, 'wb+') as f:
            
            # join output buffer to single string
            bits = ''.join(output_buffer)
            
            alignment_bits = 0
            while len(bits) % 8 != 0:
                bits += '0'
                alignment_bits += 1

            # header contains values of 'alignment_bits', 'm' and 'c'
            bin_alignmet_bits = alignment_bits.to_bytes(1, byteorder='big')
            bin_m = m.to_bytes(1, byteorder='big')
            bin_c = c.to_bytes(1, byteorder='big')
            
            f.write(bin_alignmet_bits)
            f.write(bin_m)
            f.write(bin_c)
            f.write(bitstring.BitArray(bin=bits).bytes)
            
        return enc_path
            

    def decode(self, filename: str, debug=False):
        '''
        Decodes output stream
        '''
        print(f'------dec -> {filename}------')
        # start timer
        start = time.time()
        
        bitstream = bitstring.BitArray(filename=filename).bin
        
        alignemt_bits = int(bitstream[:8], 2)
        m = int(bitstream[8:16], 2)
        c = int(bitstream[16:24], 2)
        bits = bitstream[24:len(bitstream) - alignemt_bits]

        if debug:
            print(f'bits: {bits}')
            print(f'alignement: {alignemt_bits}')
            print(f'm: {m}')
            print(f'c: {c}')

        size = len(bits)
        start = 0
        symbols = []
        while True:
            index = bits.find('0', start)
            
            # 'q' will be the number of ones until a zero is found (unary-code)
            q = index - start
            # print(f'q:{q}')

            # 'r' is the next 'c' bits
            r = bits[index + 1:index + 1 + c]
            #print(f'r:{r}')

            # relocate index
            index = index + c + 1
            # print(f'index:{index}')

            start = index
            # print(f'start:{start}')

            # compute symbol from q and r
            if r:
                symbol = int(q * m + int(r, 2) - (math.pow(2, c) - m))
            else:
                symbol = int(q * m - (math.pow(2, c) - m))
            
            symbols.append(symbol)
            
            if index >= size:
                break

        seq = ''
        i = 0
        for symbol in symbols:
            seq += '0' * symbol
            if (i != len(symbols) - 1):
                seq += '1'
            i += 1
            
        # no alignemt is needed for decoding sice it must be the exact same file as pre-encoded

        # terminate timer
        end = time.time()
        elapsed = end - start
        print(f'Decoding-Time: ~{int(elapsed)} seconds')
        
        dec_path = self.dec_path(filename)
        with open(dec_path, 'wb+') as f:
            f.write(bitstring.BitArray(bin=seq).bytes)


        
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
        return math.ceil(self.__next_power_of_two(-(math.log(1 + p) / math.log(p))))

    
    def __next_power_of_two(self, x: float) -> int:
        '''
        '''
        return 1 if x == 0 else 2**math.ceil(math.log2(x))


    def __p(self, bitstream: bitstring.BitArray.bin, zero_count: int) -> float:
        '''
        '''
        return zero_count / len(bitstream)


    def __symbol_seq(self, bitstream: bitstring.BitArray.bin) -> tuple[list[int], int]:
        '''
        Calculates sequence of zeros 
        '''
        b = bitstream
        buffer = []
        count = 0

        for s in b.split('1'):
            count += len(s) # save zero count for future reference
            buffer.append(len(s))

        return buffer, count

# https://bitstring.readthedocs.io/en/stable/slicing.html
# https://michaeldipperstein.github.io/rice.html
