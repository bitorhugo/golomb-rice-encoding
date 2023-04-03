import os, math, bitstring, csv, time


class GolombRice():
    

    __ZERO_SEQ_PATH = 'data/helper/zero-seq.csv'
    __zero_count = 0

        
    def __init__(self, file: str, debug: bool=False, test: bool=False) -> None:
        '''
        '''
        if test:
            self.__bitstream = bitstring.BitArray('0b000001001100010100000111010001')
        else:
            self.__bitstream = bitstring.BitArray(filename=file)
        self.__zero_seq(debug)

        
    def encode(self, debug: bool=False):
        '''
        Encodes input stream
        '''
        # fist calculate p(0)
        p = self.p()
        if debug:
            print(f'p:{p}')
        # second calculate m()
        m = self.m()
        if debug:
            print (f'm:{m}')
        with open(self.__ZERO_SEQ_PATH) as f:
            reader = csv.reader(f)
            next(reader) # discard csv headers
            for row in reader:
                n = int(row.pop())
                if debug:
                    print(f'n:{n}')
                    # third calculate q iteratively
                    q_int, q_unar = self.q(n, m) # q is a tuple containing its integer value and its unary representation
                    if debug:
                        print(f'q:{(q_int, q_unar)}')
                        # fourth calculate remainder with c bits
                        r = self.r(n, q_int, m, debug=True)
                        # lastly concat q and r
                        cod = str(q_unar) + str(r)
                        if (debug):
                            print(f'cod:{cod}')

                
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

        
    def r(self, n: int, q: int, m: int, debug: bool=False) -> int:
        '''
        Calculates remainder and returns it in 'c' amount of bits
        '''
        r = str(n - (q * m))
        c = self.c(m)
        padding = len(r) - c
        r = r.rjust(padding, '0')
        if debug:
            print(f'r:{r}')
        return int(r)

    
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
        print(f'zero:{self.__zero_count}')
        return self.__zero_count / len(self.__bitstream.bin)


    def __zero_seq(self, debug: bool):
        '''
        '''
        start = time.time()
        b = self.__bitstream.bin
        # check to see if file exists before computing sequence of zeros
        with open(self.__ZERO_SEQ_PATH, 'w+') as f:
            w = csv.writer(f)
            w.writerow(['number-of-zeros'])
            for s in b.split('1'):
                self.__zero_count += len(s) # save zero count for future reference
                w.writerow([len(s)])
        end = time.time()
        elapsed = end - start
        if debug:
            print(f'elapsed:{elapsed}')
            
# https://bitstring.readthedocs.io/en/stable/slicing.html
