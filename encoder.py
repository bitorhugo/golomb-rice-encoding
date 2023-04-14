import math, bitstring, csv, time


class GolombRice():
    

    # __ZERO_SEQ_PATH = 'data/helper/zero-seq.csv'
    __zero_count = 0

    zero_buffer = []
    encoding_buffer = []
        
    def __init__(self, input_file: str, debug: bool=False) -> None:
        '''
        '''
        self.__bitstream = bitstring.BitArray(filename=input_file)
        self.__zero_seq()

        
    def encode(self, debug: bool=False):
        '''
        Encodes input stream
        '''
        start = time.time()
        # fist calculate p(0)
        # p = self.p()
        # if debug:
        #     print(f'p:{p}')
        # second calculate m()
        m = self.m()
        if debug:
            print (f'm:{m}')
        # with open(self.__ZERO_SEQ_PATH) as f:
        #     reader = csv.reader(f)
        #     next(reader) # discard csv headers
        for row in self.zero_buffer:
            n = int(row)
            if debug:
                print(f'n:{n}')
            # third calculate q iteratively
            q_int, q_unar = self.q(n, m) # q is a tuple containing its integer value and its unary representation
            if debug:
                print(f'q:{(q_int, q_unar)}')
            # fourth calculate remainder with c bits
            r = self.r(n, q_int, m, debug=debug)
            # lastly concat q and r
            cod = str(q_unar) + r
            self.encoding_buffer.append(cod)

        end = time.time()
        elapsed = end - start
        print(f'Time:{int(elapsed)}s')
        
        with open('data/encodings/test', 'w+') as f:
            f.writelines(self.encoding_buffer)

                
    def decode(self):
        '''
        Decodes output stream
        '''
        pass


    def c(self, m: int) -> int:
        '''
        Calculates the amount of bits necessary to represent r
        '''
        return math.ceil(math.log2(m))

        
    def r(self, n: int, q: int, m: int, debug: bool=False) -> str:
        '''
        Calculates remainder and returns it in 'c' amount of bits
        '''
        r = n - q * m
        r_bin = bin(r)[2:]
        # print(f'r:{r_bin}')
        c = self.c(m)
        # print(f'c:{c}')
        padding = c - len(r_bin)
        # print (padding)

        if padding > 0:
            r_bin = r_bin.zfill(c)
            # print (r_bin)

        return r_bin

    
    def q(self, n: int, m: float) -> tuple[int, str]:
        '''
        Calculates quoficient and returns it as unary
        q = n / m, rounded to the floor
        '''
        q = math.floor( n/m )
        unary = ''
        for _ in range(q):
            unary += '1'
        unary += '0'
        return (q, unary)


    def m(self) -> int:
        '''
        m is a formula that will be rounded to the nearest base 2 exponential value
        m = -log(1+zero_prob)/log(zero_prob)
        '''
        p = self.p()
        return math.ceil(self.__next_power_of_two(-math.log(1 + p) / math.log(p)))

    
    def __next_power_of_two(self, x: float) -> int:
        '''
        '''
        return 1 if x == 0 else 2**math.ceil(math.log2(x))


    def p(self) -> float:
        '''
        '''
        return self.__zero_count / len(self.__bitstream.bin)


    def __zero_seq(self):
        '''
        Calculates sequence of zeros 
        '''
        b = self.__bitstream.bin
        start = time.time() # set timer
        for s in b.split('1'):
            self.__zero_count += len(s) # save zero count for future reference
            self.zero_buffer.append(len(s))
        # check to see if file exists before computing sequence of zeros
        # with open(self.__ZERO_SEQ_PATH, 'w+') as f:
        #     w = csv.writer(f)
        #     w.writerow(['number-of-zeros'])
        #     for s in b.split('1'):
        #         self.__zero_count += len(s) # save zero count for future reference
        #         w.writerow([len(s)])
        end = time.time()
        elapsed = end - start
        print(f'zero-seq-time:{elapsed}')
            
# https://bitstring.readthedocs.io/en/stable/slicing.html
