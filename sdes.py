from utilities import *
from math import *
from copy import *

class SBOX:
    """
    ----------------------------------------------------
    Description: SDES SBOX
    ----------------------------------------------------
    """
    def __init__(self,box):
        """
        ----------------------------------------------------
        config:   box (list): a 2D list of size 2x8 containing binary numbers
        Description:  Creates an SBOX object from given 2D lists
                      Assume the user will always provide a valid box
        ---------------------------------------------------
        """
        self.box=box
        return
            
    def __getitem__(self,value):
        """
        ----------------------------------------------------
        Magic Method
        allows using the sbox object s in the following manner s['1001']
        config:   in_num (str): binary number of 4 bits
        Return:       out_num (str): binary number of 3 bits
        Description:  computes the SBOX value of in_num
                      if in_num is invalid returns ''
        ---------------------------------------------------
        """ 
        if not isinstance(value, str):
            return ''
        
        if len(value)!=4 or not all(char in '01' for char in value):
            return ''
        
        row=value[0]
        col=value[1:]
        row=bin_to_dec(row)
        col=bin_to_dec(col)
        return self.box[row][col]
    
    def __str__(self):
        """
        ----------------------------------------------------
        config:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of SBOX object
                      format:
                      <row 0 of _box>
                      <row 1 of _box>
        ---------------------------------------------------
        """ 

            
        return str(self.box[0]) + '\n' +  str(self.box[1])

class SDES:
    DEFAULT_ENCODING = 'B6'
    DEFAULT_BLOCK_SIZE = 12
    DEFAULT_KEY_LENGTH = 9
    DEFAULT_ROUNDS = 2
    DEFAULT_P = 103
    DEFAULT_Q = 199
    DEFAULT_SBOX1 = SBOX([['101','010','001','110','011','100','111','000'],
            ['001','100','110','010','000','111','101','011']])
    DEFAULT_SBOX2 = SBOX([['100','000','110','101','111','001','011','010'],
            ['101','011','000','111','110','010','001','100']])
    DEFAULT_PAD = 'Q'
    DEFAULT_PRIMES_FILE = 'primes.txt'

    @staticmethod
    def gcd(a,b):
        """
        ----------------------------------------------------
        Static Method
        config:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       result (int): gcd(a,b)
        Description:  Computes and returns the greatest common divider using
                      the standard Eculidean Algorithm.
                      The implementation can be iterative or recursive
        Errors:       if a or b are non positive integers, return:
                        'Error(SDES.gcd): invalid input'
        ---------------------------------------------------
        """
        if not isinstance(a,int) or not isinstance(b,int):
            return 'Error(SDES.gcd): invalid input'
        if a==0 or b==0:
            return 'Error(SDES.gcd): invalid input'
        a=abs(a)
        b=abs(b)
        while b!=0:
            a,b=b,a%b

        return a

    @staticmethod
    def is_prime(n):
        """
        ----------------------------------------------------
        Static Method
        config:   n (int): an arbitrary integer
        Return:       True/False
        Description:  Check if the given input is a prime number
                    Search Online for an efficient implementation
        ---------------------------------------------------
        """
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    
    @staticmethod
    def is_relatively_prime(a,b):
        """
        ----------------------------------------------------
        Static Method
        config:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       True/False
        Description:  Check if <a> and <b> are relatively prime
                          i.e., gcd(a,b) equals 1
        Errors:       if <a> or <b> are non positive integers, return:
                        'Error(SDES.is_relatively_prime): invalid input'
        ---------------------------------------------------
        """
        if not isinstance(a,int) or not isinstance(b,int) or a<0 or b<0:
            return 'Error(SDES.is_relatively_prime): invalid input'
        if gcd(a,b)==1:
            return True
        return False

    @staticmethod
    def BBS(p,q,bits,primes_file):
        """
        ----------------------------------------------------
        config:   p (int): a prime number
                      q (int): a prime number
                      bits (int): number of bits to generate
        Return:       output (str): stream of random binary bits
        Description:  Blum Blum Shub PRNG Generator
                      p and q should be primes congruent to 3
                      The seed is the nth prime number, where n = p*q
                      If the nth prime number is not relatively prime with n,
                          the next prime number is selected until a valid one is found
                          The prime numbers are read from the file PRIMES_FILE (starting n=1)
                      If invalid input --> return error message
        ---------------------------------------------------
        """ 

        if type(p)!=int or p%4!=3:
         return 'Error(SDES.BBS): invalid p'
        if type(q)!=int or q%4!=3:
            return 'Error(SDES.BBS): invalid q'
        if type(bits)!=int or bits<=0:
            return 'Error(SDES.BBS): invalid bits'
        
        n=p*q
        primenums=file_to_text(primes_file).split('\n')
        seed=int(primenums[int(n-1)])
        end=n
        while not SDES.is_relatively_prime(n,seed):
            seed=primenums[end]
            end+=1
        x=(seed*seed) % n
        output=''
        for _ in range(bits):
            x=(x*x)%n
            output+=str(x%2)
        return output
                
    def __init__(self,config={}):
        """
        ----------------------------------------------------
        Parameters:   config(dict): SDES parameters
                          rounds (int)
                          key_length (int)
                          block_size (int)
                          encoding (str)
                          p (int)
                          q (int)
                          sbox1 (SBOX)
                          sbox2 (SBOX)
                          pad (str)
                          primes_file (str)
        Description:  Constructs an SDES object
                          The object maintains a config dictionary set to the given values
                          missing parameters are set to default values
                          Assume if parameters are given, then they are valid values
        ---------------------------------------------------
        """
        self.config = {
            'rounds': config.get('rounds', SDES.DEFAULT_ROUNDS),
            'key_length': config.get('key_length', SDES.DEFAULT_KEY_LENGTH),
            'block_size': config.get('block_size', SDES.DEFAULT_BLOCK_SIZE),
            'encoding': config.get('encoding', SDES.DEFAULT_ENCODING),
            'p': config.get('p', SDES.DEFAULT_P),
            'q': config.get('q', SDES.DEFAULT_Q),
            'sbox1': config.get('sbox1', SDES.DEFAULT_SBOX1),
            'sbox2': config.get('sbox2', SDES.DEFAULT_SBOX2),
            'pad': config.get('pad', SDES.DEFAULT_PAD),
            'primes_file': config.get('primes_file', SDES.DEFAULT_PRIMES_FILE)
        }

        
    def get_config_value(self,parameter):
        """
        ----------------------------------------------------
        config:   parameter (str)
        Return:       value (?)
        Description:  Returns a copy of parameter value
                      Valid parameter names:
                      rounds, key_length, block_size, encoding,
                      p, q, sbox1, sbox2, pad, primes_file
                      if invalid parameter name --> print return ''
        ---------------------------------------------------
        """
        if not isinstance(parameter,str):
            return ''
        if parameter not in self.config:
            return ''
        else:
            return self.config[parameter]
    
    def set_parameter(self,parameter,value):
        """
        ----------------------------------------------------
        config:   parameter (str)
                      value (?)
        Return:       success: True/False
        Description:  Set the given parameter to given value (if valid)
                      if invalid parameter/value, do not update current value and return False
                      if valid parameter+valid, update value and return True
                          rounds should be an integer larger than 1
                          p and q should be integers congruent to 3 mod 4
                          pad should be a single character string in B6 encoding
                          sbox1 and sbox2 should be SBOX objects
                          block_size should be an integer of multiples of 2, >= 4
                          Cannot set key_length or encoding
                          Note: when block_size is set:
                              key_length is set to block_size//2 + 3
                          primes_file: should be a valid filename that exists in the same directory
        ---------------------------------------------------
        """

        if parameter == 'rounds':
            if isinstance(value, int):
                if value > 1:
                    self.config['rounds'] = value
                    return True
        elif parameter in ['p', 'q']:
            if isinstance(value, int): 
                if value % 4 == 3 and self.is_prime(value):
                    self.config[parameter] = value
                    return True
        elif parameter == 'pad':
            if isinstance(value, str): 
                if len(value) == 1:
                    if value in get_base('B6'):
                        self.config['pad'] = value
                        return True
        elif parameter in ['sbox1', 'sbox2']:
            if isinstance(value, SBOX):
                self.config[parameter] = value
                return True
        elif parameter == 'block_size':
            if isinstance(value, int):
                if value >= 4:
                    if (value & (value - 1)) == 0:
                        self.config['block_size'] = value
                        self.config['key_length'] = value // 2 + 3
                        return True
        elif parameter == 'primes_file':
            try:
                with open(value, 'r'):
                    self.config['primes_file'] = value
                    return True
            except IOError:
                return False
        return False

    def __str__(self):
        """
        ----------------------------------------------------
        config:   -
        Return:       output (str): 
        Description:  returns a string representation of the current SDES object:
                        SDES Configuration:
                        rounds = <rounds>
                        key_length = <key_length>
                        block_size = <block_size>
                        encoding = <encoding>
                        sbox1 = <sbox1>
                        sbox2 = <sbox2>
                        p = <p>
                        q = <q>
                        pad = <pad>
                        primes_file = <primes_file>
                        
        ---------------------------------------------------
        """
        return (f"SDES Configuration:\n"
                f"rounds = {self.config['rounds']}\n"
                f"key_length = {self.config['key_length']}\n"
                f"block_size = {self.config['block_size']}\n"
                f"encoding = {self.config['encoding']}\n"
                f"p = {self.config['p']}\n"
                f"q = {self.config['q']}\n"
                f"sbox1 = {self.config['sbox1']}\n"
                f"sbox2 = {self.config['sbox2']}\n"
                f"pad = {self.config['pad']}\n"
                f"primes_file = {self.config['primes_file']}\n")
            
    def get_key(self):
        """
        ----------------------------------------------------
        config:   -
        Return:       key (str): binary number
        Description:  Returns a copy of SDES key
                      The key is generated by Blum Blum Shub algorithm
                      Uses p and q to generate key_length bits
        ---------------------------------------------------
        """
        
        return SDES.BBS(self.config['p'], self.config['q'],self.config['key_length'], self.config['primes_file'] )
    
    def get_subkey(self,i):
        """
        ----------------------------------------------------
        config:   i (int): subkey index
        Return:       subkey (str): binary number
        Description:  Returns the ith subkey from SDES key
                      Gets key_length bits from key starting at index i
                      Using circular indexing if necessary
        Errors:       if invalid i --> return ''
        ---------------------------------------------------
        """
        key = self.get_key()
        if not (isinstance(i, int) and 0 < i):
            return ''
        shiftkey = shift_str(key, i-1, 'l')
        subkey = shiftkey[:self.config['key_length'] - 1]
        return subkey
        
        
    def expand(self,R):
        """
        ----------------------------------------------------
        config:   R (str): binary number of size (block_size/2)
        Return:       R_exp (str): output of expand function
        Description:  Expand the input binary number by adding two digits
                      Expansion works as the following:
                      If the index of the two middle elements is i and i+1
                          indices 0 up to i-1: same order
                          middle becomes: R(i+1)R(i)R(i+1)R(i)
                          indices R(i+2) to the end: same order
                      No need to validate that R is of size block_size/2
        Errors:       if R is an invalid binary number -->  return ''
        ---------------------------------------------------
        """
        if not is_bin(R):
            return ''
        i = len(R) // 2
        R_exp = R[:i-1]+R[i]+R[i-1]+R[i]+R[i-1]+R[i+1:]

        return R_exp
    
    def F(self,Ri,ki):
        """
        ----------------------------------------------------
        config:   Ri (str): block of binary numbers
                      ki (str): binary number representing subkey
        Return:       Ri2 (str): block of binary numbers
        Description:  Performs the following five tasks:
                      1- Pass the Ri block to the expander function
                      2- Xor the output of [1] with ki
                      3- Divide the output of [2] into two equal sub-blocks
                      4- Pass the most significant bits of [3] to Sbox1
                         and least significant bits to sbox2
                      5- Concatenate the output of [4] as [sbox1][sbox2]
        Errors:       if ki or Ri is an invalid binary number --> return ''
        ---------------------------------------------------
        """
        if not is_bin(ki) or not is_bin(Ri):
            return '' 
        R_exp=self.expand(Ri)
        if len(R_exp) !=len(ki):
            return ''
        O=xor(R_exp,ki)
        left_half=O[:len(O)//2]
        right_half=O[len(O)//2:]
        self.set_parameter('sbox1',left_half)
        self.set_parameter('sbox2',right_half)
        sbox1_output = self.config['sbox1'][left_half]
        sbox2_output = self.config['sbox2'][right_half]
        Ri=sbox1_output+sbox2_output
        return Ri


    def feistel(self,bi,ki):
        """
        ----------------------------------------------------
        config:   bi (str): block of binary numbers
                      ki (str): binary number representing subkey
        Return:       bi2 (str): block of binary numbers
        Description:  Applies Feistel Cipher on a block of binary numbers
                      L(current) = R(previous)
                      R(current) = L(previous) xor F(R(previous), subkey)
        Errors:       if ki or bi is an invalid binary number --> return ''
        ---------------------------------------------------
        """
        if not isinstance(bi, str) or not isinstance(ki, str):
            return ''
        if not is_bin(bi) or not is_bin(ki):
            return ''
        if len(bi) % 2 != 0 or len(ki) == 0 or len(ki)%2!=0:
            return ''
        
        leftblock=bi[:len(bi)//2]
        rightblock=bi[len(bi)//2:]
        newright=self.F(rightblock,ki)
        newleft=xor(leftblock,newright)
        bi2=rightblock+newleft
        return bi2
        
    def encrypt(self,plaintext,mode):
        """
        ----------------------------------------------------
        config:   plaintext (str)
                      mode (str)
        Return:       ciphertext (str)
        Description:  A dispatcher SDES encryption function
                      passes the plaintext to the proper function based on given mode
                      Works for ECB, CBC and OFB modes
        Errors:       if undefined mode --> return ''
        ---------------------------------------------------
        """
        charset=get_char_indexes(plaintext, '\n')
        plaintext=remove_chars(plaintext,'\n')
        charset1=get_char_indexes(plaintext, '.')
        plaintext=remove_chars(plaintext,'.')
        ciphertext=''
        if mode=='ECB':
            ciphertext=self._encrypt_ECB(plaintext)
            ciphertext=restore_text(ciphertext,charset1)
            ciphertext=restore_text(ciphertext,charset)
            return ciphertext
        if mode=='CBC':
            ciphertext=self._encrypt_CBC(plaintext)
            ciphertext=restore_text(ciphertext,charset1)
            ciphertext=restore_text(ciphertext,charset)
            return ciphertext
        if mode=='OFB':
            ciphertext=self._encrypt_OFB(plaintext)
            ciphertext=restore_text(ciphertext,charset1)
            ciphertext=restore_text(ciphertext,charset)
            return ciphertext
        ciphertext=restore_text(ciphertext,charset1)
        ciphertext=restore_text(ciphertext,charset)
        return ''
        
    
    def decrypt(self,ciphertext,mode):
        """
        ----------------------------------------------------
        config:   ciphertext (str)
                      mode (str)
        Return:       plaintext (str)
        Description:  A dispatcher SDES decryption function
                      passes the ciphertext to the proper function based on given mode
                      Works for ECB, CBC and OFB modes
        Errors:       if undefined mode --> return ''
        ---------------------------------------------------
        """
        charset=get_char_indexes(ciphertext, '\n')
        ciphertext=remove_chars(ciphertext,'\n')
        charset1=get_char_indexes(ciphertext, '.')
        ciphertext=remove_chars(ciphertext,'.')
        if mode=='ECB':
            plaintext=self._decrypt_ECB(ciphertext)
            plaintext=restore_text(plaintext,charset1)
            plaintext=restore_text(plaintext,charset)
            return plaintext
        if mode=='CBC':
            plaintext=self._decrypt_CBC(ciphertext)
            plaintext=restore_text(plaintext,charset1)
            plaintext=restore_text(plaintext,charset)
            return plaintext
        if mode=='OFB':
            plaintext=self._decrypt_OFB(ciphertext)
            plaintext=restore_text(plaintext,charset1)
            plaintext=restore_text(plaintext,charset)
            return plaintext
        
        return ''
    
    def _encrypt_ECB(self,plaintext):
        """
        ----------------------------------------------------
        config:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using ECB mode
        ---------------------------------------------------
        """
        ciphertext=''
        pad=self.config['pad']
        special_chars_positions = []
        for char in plaintext:
            if char not in get_base(self.config['encoding']):
                special_chars_positions.append(get_char_indexes(plaintext, char))
                plaintext=remove_chars(plaintext, char)

        cleaned_plaintext=plaintext

        blocks = [cleaned_plaintext[i:i+2] for i in range(0, len(cleaned_plaintext), 2)]
        encrypted_blocks=[]
        pad=encode(pad,self.config['encoding'])
        for block in blocks:
            text=encode(block,self.config['encoding'])
            while len(text)%self.config['block_size']!=0:
                text+=pad
            for i in range(self.config['rounds']):
                text=self.feistel(text, self.get_subkey(i+1))

            right,left=text[:len(text)//2], text[len(text)//2:]
            text=left+right

            encrypted_blocks.append(text)

            bincipher=''.join(encrypted_blocks)
            ciphertext=decode(bincipher, self.config['encoding'])
        # Restoring the special characters in the ciphertext:
        for i in range(len(special_chars_positions)-1,-1,-1):
            ciphertext=restore_text(ciphertext,special_chars_positions[i])
        return ciphertext
    
    def _decrypt_ECB(self,ciphertext):
        """
        ----------------------------------------------------
        config:   ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using ECB mode
        ---------------------------------------------------
        """
        plaintext = ''
        special_chars_positions = []
        base = get_base(self.config['encoding'])
        
        # Identify and remove special characters from the ciphertext
        for char in ciphertext:
            if char not in base:
                special_chars_positions.append(get_char_indexes(ciphertext, char))
                ciphertext = remove_chars(ciphertext, char)
        
        cleaned_ciphertext = ciphertext
        
        # Split ciphertext into blocks
        blocks = [cleaned_ciphertext[i:i + 2] for i in range(0, len(cleaned_ciphertext), 2)]
        decrypted_blocks = []
        
        # Decode each block and decrypt using Feistel network
        for block in blocks:
            text = encode(block, self.config['encoding'])
            for i in range(self.config['rounds'], 0, -1):
                text = self.feistel(text, self.get_subkey(i))
            
            right, left = text[:len(text) // 2], text[len(text) // 2:]
            text = left + right
            decrypted_blocks.append(text)
        
        # Combine decrypted blocks and decode
        bin_plaintext = ''.join(decrypted_blocks)
        plaintext = decode(bin_plaintext, self.config['encoding'])
        
        # Remove padding if present
        plaintext = plaintext.rstrip(self.config['pad'])
        
        # Restore special characters in the plaintext
        for i in range(len(special_chars_positions) - 1, -1, -1):
            plaintext = restore_text(plaintext, special_chars_positions[i])
        
        return plaintext

    def _encrypt_CBC(self,plaintext):
        """
        ----------------------------------------------------
        config:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using CBC mode
        ---------------------------------------------------
        """
        plaintext=plaintext.strip()
        ciphertext=''
        pad=self.config['pad']
        special_chars_positions = []
        for char in plaintext:
            if char not in get_base(self.config['encoding']):
                special_chars_positions.append(get_char_indexes(plaintext, char))
                plaintext=remove_chars(plaintext, char)
        
        cleaned_plaintext=plaintext
        blocks = [cleaned_plaintext[i:i+2] for i in range(0, len(cleaned_plaintext), 2)]
        encrypted_blocks=[]
        pad=encode(pad,self.config['encoding'])
        blockxor=self._get_IV()
        for block in blocks:
            text=encode(block,self.config['encoding'])
            while len(text)%self.config['block_size']!=0:
                text+=pad
            text=xor(text,blockxor)
            for i in range(self.config['rounds']):
                text=self.feistel(text, self.get_subkey(i+1))

            right,left=text[:len(text)//2], text[len(text)//2:]
            CT=left+right
            
            encrypted_blocks.append(CT)
            blockxor=CT
            bincipher=''.join(encrypted_blocks)
            ciphertext=decode(bincipher, self.config['encoding'])
        # Restoring the special characters in the ciphertext:
        for i in range(len(special_chars_positions)-1,-1,-1):
            ciphertext=restore_text(ciphertext,special_chars_positions[i])
        return ciphertext
    
    def _get_IV(self):
        """
        ----------------------------------------------------
        config:   -
        Return:       iv (str): binary number
        Description:  prepares an IV for CBC and OFB modes
                      the IV length is the same as the block size
                      the IV is a stream of bits that follow the following pattern:
                      1 00 111 0000 11111 ...
        ---------------------------------------------------
        """ 
        IV=''
        i=1
        while len(IV)<self.config['block_size']:
            if i%2!=0:
                IV+='1'*i
            else:
                IV+='0'*i
            i+=1
        return IV[:self.config['block_size']]

    def _decrypt_CBC(self,ciphertext):   
        """
        ----------------------------------------------------
        config:       ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using CBC mode
        ---------------------------------------------------
        """
        plaintext = ''
        special_chars_positions = []
        base = get_base(self.config['encoding'])
        
        # Identify and remove special characters from the ciphertext
        for char in ciphertext:
            if char not in base:
                special_chars_positions.append(get_char_indexes(ciphertext, char))
                ciphertext = remove_chars(ciphertext, char)
        
        cleaned_ciphertext = ciphertext
        
        # Split ciphertext into blocks
        blocks = [cleaned_ciphertext[i:i + 2] for i in range(0, len(cleaned_ciphertext), 2)]
        decrypted_blocks = []
        
        # Decode each block and decrypt using Feistel network
        for block in blocks:
            text = encode(block, self.config['encoding'])
            for i in range(self.config['rounds'], 0, -1):
                text = self.feistel(text, self.get_subkey(i))
            
            right, left = text[:len(text) // 2], text[len(text) // 2:]
            PT = left + right
            if block==blocks[0]:
                text=xor(PT,self._get_IV())
            else:
                text=xor(PT,blockxor)
            blockxor=encode(block,self.config['encoding'])
            decrypted_blocks.append(text)
            
        
        # Combine decrypted blocks and decode

        bin_plaintext = ''.join(decrypted_blocks)
        plaintext = decode(bin_plaintext, self.config['encoding'])
        
        # Remove padding if present
        plaintext = plaintext.rstrip(self.config['pad'])
        
        # Restore special characters in the plaintext
        for i in range(len(special_chars_positions) - 1, -1, -1):
            plaintext = restore_text(plaintext, special_chars_positions[i])
        
        return plaintext


    def _encrypt_OFB(self,plaintext):
        """
        ----------------------------------------------------
        config:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using OFB mode
        ---------------------------------------------------
        """
        Nonce=self._get_IV()
        plaintext=plaintext.strip()
        ciphertext=''
        pad=self.config['pad']
        special_chars_positions = []
        for char in plaintext:
            if char not in get_base(self.config['encoding']):
                special_chars_positions.append(get_char_indexes(plaintext, char))
                plaintext=remove_chars(plaintext, char)

        cleaned_plaintext=plaintext

        blocks = [cleaned_plaintext[i:i+2] for i in range(0, len(cleaned_plaintext), 2)]
        encrypted_blocks=[]
        pad=encode(pad,self.config['encoding'])
        for block in blocks:
            text=encode(block,self.config['encoding'])
            for i in range(self.config['rounds']):
                Nonce=self.feistel(Nonce, self.get_subkey(i+1))

            right,left=Nonce[:len(Nonce)//2], Nonce[len(Nonce)//2:]
            Nonce=left+right
            ct=xor(Nonce[:len(text)], text)
            encrypted_blocks.append(ct)

            bincipher=''.join(encrypted_blocks)
            ciphertext=decode(bincipher, self.config['encoding'])
        # Restoring the special characters in the ciphertext:
        for i in range(len(special_chars_positions)-1,-1,-1):
            ciphertext=restore_text(ciphertext,special_chars_positions[i])
        return ciphertext

    def _decrypt_OFB(self, ciphertext):
        """
        ----------------------------------------------------
        config:       ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using OFB mode
        ---------------------------------------------------
        """
        Nonce = self._get_IV()
        ciphertext = ciphertext.strip()
        plaintext = ''
        pad = self.config['pad']
        block_size = 2  # Assuming blocks of 2 characters for simplicity
        special_chars_positions = []

        for char in ciphertext:
            if char not in get_base(self.config['encoding']):
                special_chars_positions.append(get_char_indexes(ciphertext, char))
                ciphertext = remove_chars(ciphertext, char)

        cleaned_ciphertext = ciphertext
        blocks = [cleaned_ciphertext[i:i+block_size] for i in range(0, len(cleaned_ciphertext), block_size)]
        decrypted_blocks = []

        for block in blocks:
            text = encode(block, self.config['encoding'])
            for i in range(self.config['rounds']):
                Nonce = self.feistel(Nonce, self.get_subkey(i+1))

            right, left = Nonce[:len(Nonce)//2], Nonce[len(Nonce)//2:]
            Nonce = left + right
            pt = xor(Nonce[:len(text)], text)
            decrypted_blocks.append(pt)

        binplaintext = ''.join(decrypted_blocks)
        plaintext = decode(binplaintext, self.config['encoding'])

        # Restoring the special characters in the plaintext:
        for i in range(len(special_chars_positions)-1, -1, -1):
            plaintext = restore_text(plaintext, special_chars_positions[i])
        
        # Remove padding if any
        plaintext = plaintext.rstrip(pad)
        
        return plaintext

