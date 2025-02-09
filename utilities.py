from math import ceil

def get_base(encoding):
    """
    ----------------------------------------------------
    Parameters:   encoding (str) 
    Return:       result (str)
    Description:  Return string containing all characters defined in the given encoding
                  Defined base types:
                      lower: lower case characters
                      upper: upper case characters
                      alpha: upper and lower case characters
                      lowernum: lower case and numerical characters
                      uppernum: upper case and numerical characters
                      alphanum: upper, lower and numerical characters
                      special: punctuation and special characters (no white spaces)
                      nonalpha: special and numerical characters
                      B6: lower, uppper, num, dot, space
                      BA: upper + lower + num + special + ' \n'
                      pascii: upper, lower, numerical and special characters
                      unicode128: pascii + few unicode characters
                      unicode256: pascii + many unicode characters
                      whitespaces: ' ' + \n + \r + \t
    Errors:       if invalid encoding, print error msg, return empty string
    ---------------------------------------------------
    """
    lower = "".join([chr(ord('a')+i) for i in range(26)])
    upper = lower.upper()
    num = "".join([str(i) for i in range(10)])
    alpha = upper + lower
    special = ''
    for i in range(ord('!'),127):
        if not chr(i).isalnum():
            special+= chr(i)
    
    unicode1 = 'ÄÆÑÓÙÝäß£¥Ø±÷«»×©ŖŴŽģΔΓΠΦΨδϪΩω¶♤∫₡'
    unicode2 = '❤♫☎♨✈☀✂☑✉☆✎♕✍♂♀ϨϾЊжѠ😀😂😌😛😣😎😔😥😱😬😳😸🙄🙈🙌🙏😈✌❌➔➶🌍🌩🌭🌽🍉🌲🍄🍔🍩🍼🍽🎒🎧'
    unicode2 += '⚙⚠⚰⚽⚿⛍⛔⛏⛵⛷🎤⚀⚂⚄♲⚓⚖∋∌∛∧∨∩∪∲∴∵∻≂≄≡≤≥⊂⊃⊄⊞⊠⊤⊥⊻⊼⊿⋇⋈⋉⋐⋓▦◐◍◢◥◪◆◎☂☃☍☁☕☝☠☢☪☹☺♔♖♙♘🎮🏍🏠'
    result = ''
    if encoding == 'lower': #26 chars
        result = lower
    elif encoding == 'upper': #26 chars
        result = upper
    elif encoding == 'alpha': #52 chars
        result = alpha
    elif encoding == 'lowernum': #36 chars
        result = lower + num
    elif encoding == 'uppernum': #36 chars
        result = upper + num
    elif encoding == 'alphanum': #62
        result = alpha + num
    elif encoding == 'special': #32 chars
        result = special
    elif encoding == 'nonalpha': #42
        result = special + num
    elif encoding == 'B6': #64 symbols
        result = lower + upper + num + '.' + ' '
    elif encoding == 'BA': #96 symbols
        result = alpha + num + special + ' \n'
    elif encoding == 'pascii': #94 printable ASCII characters
        result = alpha + num + special
    elif encoding == 'unicode128': #128
        result = alpha + num + special + unicode1
    elif encoding == 'unicode256': #256 chars
        result = alpha + num + special + unicode1 + unicode2
    elif encoding == 'whitespaces':
        result = ' \n\t\r'
    else:
        print('Error(get_base): undefined base type')
        result = ''
    return result

'______________________________________________________________________________'

def is_bin(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       True/False
    Description:  Checks if given input is a string that represent a valid
                  binary number
                  Valid strings: '1101' and '0b101'
                  An empty string, or a string that contains other than 0 or 1
                  should return False
    ---------------------------------------------------
    """
    # if type(b) != str or len(b) == 0:
    #     return False
    # if len(b) >=2 and b[:2] == '0b':
    #     b = b[2:]
    # if set(b) == set('10'):
    #     return True
    # return False
    if type(b) != str:
        return False
    if len(b) >= 2:
        if b[:2] == '0b':
            b = b[2:]
    if b == '':
        return False
    for i in range(len(b)):
        if b[i]!= '0' and b[i]!='1':
            return False
    return True

'______________________________________________________________________________'

def xor(a,b):
    """
    ----------------------------------------------------
    Parameters:   a (str): binary number
                  b (str): binary number
    Return:       c (str): binary number of a xor b
    Description:  Apply xor operation on a and b
    Errors:       if a or b is not a valid binary number 
                      print 'Error(xor): invalid input' and return ''
                  if a and b have different lengths:
                       print 'Error(xor): size mismatch' and return ''
    ---------------------------------------------------
    """
    try:
        if len(a) != len(b):
            print('Error(xor): size mismach')
            c = ''
        else:
            size = len(a)
            a = int('0b'+a,2)
            b = int('0b'+b,2)
            c = bin(a ^ b)[2:]
            c = '0'*(size-len(c))+c
    except Exception as e:
        print('Error(xor): {}'.format(e))
        c = ''
    return c

'______________________________________________________________________________'

def dec_to_bin(decimal,size=None):
    """
    ----------------------------------------------------
    Parameters:   decimal (int): input decimal number
                  size (int): number of bits in output binary number
                      default size = None
    Return:       binary (str): output binary number
    Description:  Converts any integer to binary
                  Result is to be represented in size bits
                  pre-pad with 0's to fit the output in the given size
                  If no size is given, no padding is done 
    Asserts:      decimal is an integer
    Errors:       if an invalid size:
                      print 'Error(dec_to_bin): invalid size' and return ''
                  if size is too small to fit output binary number:
                      print 'Error(dec_to_bin): integer overflow' and return ''
    ---------------------------------------------------
    """
    assert type(decimal) == int, 'invalid input'
    
    if (size != None and type(size) != int) or (type(size) == int and size <1):
        print('Error(dec_to_bin): invalid size')
        return ''
    
    binary = bin(decimal)[2:]
    
    if size == None or len(binary) == size:
        return binary
    
    if len(binary) > size:
        print('Error(dec_to_bin): integer overflow')
        return ''
    
    return '0'*(size-len(binary)) + binary

'______________________________________________________________________________'

def bin_to_dec(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       decimal (int)
    Description:  Converts a binary number into corresponding integer
    Exceptions:   return empty string
    ---------------------------------------------------
    """
    try:
        if b[:2] != '0b':
            b = '0b' + b
        value = int(b,2)
    except Exception:
        value = ''
    return value

'______________________________________________________________________________'

def is_valid_filename(filename):
    """
    ----------------------------------------------------
    Parameters:   filename (str)
    Return:       True/False
    Description:  Checks if given input is a valid filename 
                  a filename should have at least 3 characters
                  and contains a single dot that is not the first or last character
    ---------------------------------------------------
    """
    if type(filename) != str:
        return False
    if len(filename) < 3:
        return False
    if '.' not in filename:
        return False
    if filename[0] == '.' or filename[-1] == '.':
        return False
    if filename.count('.') != 1:
        return False
    return True

'______________________________________________________________________________'

def shift_str(s,n,d='l'):
    """
    ----------------------------------------------------
    Parameters:   text (string): input string
                  shifts (int): number of shifts
                  direction (str): 'l' or 'r'
    Return:       update_text (str)
    Description:  Shift a given string by given number of shifts (circular shift)
                  If shifts is a negative value, direction is changed
                  If no direction is given or if it is not 'l' or 'r' set to 'l'
    Asserts:      text is a string and shifts is an integer
    ---------------------------------------------------
    """
    assert type(s) == str and type(n) == int
    if d != 'r' and d!= 'l':
        d = 'l'
    if n < 0:
        n = n*-1
        d = 'l' if d == 'r' else 'r'
    n = n%len(s)
    if s == '' or n == 0:
        return s

    s = s[n:]+s[:n] if d == 'l' else s[-1*n:] + s[:-1*n]
    return s

'______________________________________________________________________________'

def get_char_indexes(text,base):
    """
    ----------------------------------------------------
    Parameters:   text (str): input string
                  base (str):  stream of unique characters
    Return:       char_indexes (2D list)
    Description:  Analyzes a given text for any occurrence of base characters
                  Returns a 2D list with characters and their respective indexes
                  format: [[char1,index1], [char2,index2],...]
                  Example: get_char_indexes('I have 3 cents.','c.h') -->
                      [['h',2],['c',9],['.',14]]
                  items are ordered based on their occurrence in the text
    Asserts:      text and base are strings
    ---------------------------------------------------
    """
    assert type(text) == str and type(base) == str, 'invalid input'
    positions = []
    for i in range(len(text)):
        if text[i] in base:
            positions.append([text[i],i])
    return positions

'______________________________________________________________________________'

def remove_chars(text,base):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  base (str)
    Return:       updated_text (str)
    Description:  Constructs and returns a new text which has
                  all characters in original text after removing base characters
    Asserts:      text and base are strings
    ---------------------------------------------------
    """
    assert type(text) == str and type(base) == str, 'invalid input'
    updated_text = ''
    for char in text:
        if char not in base:
            updated_text += char
    return updated_text

def encode(text,encoding):
    supported_encodings = ['B6','unicode128','unicode256']
    if encoding not in supported_encodings:
        print('Error(encode): unsupported encoding')
        return ''
    if encoding == 'B6':
        bits = 6
    elif encoding == 'unicode128':
        bits = 7
    elif encoding == 'unicode256':
        bits = 8
    base = get_base(encoding)
    output = ''
    for c in text:
        if c not in base:
            print(f'Error(encode): undefined character {c}')
            return ''
        indx = base.index(c)
        output += dec_to_bin(indx, bits)
    return output

def decode(code,encoding):
    supported_encodings = ['B6','unicode128','unicode256']
    if encoding not in supported_encodings:
        print('Error(decode): unsupported encoding')
        return ''
    if encoding == 'B6':
        bits = 6
    elif encoding == 'unicode128':
        bits = 7
    elif encoding == 'unicode256':
        bits = 8
    base = get_base(encoding)
    output = ''
    blocks = get_str_blocks(code, bits)
    for block in blocks:
        indx = bin_to_dec(block)
        output += base[indx]
    return output

'______________________________________________________________________________'

def get_str_blocks(string,block_size,pad =''):
    """
    ----------------------------------------------------
    Parameters:   string (str): input string
                  block_size (int)
                  pad (str): padding character, by default empty string (no padding)
    Return:       blocks (list)
    Description:  Create a list containing strings each of given block size
                  if padding used, pad last block with given character
    Asserts:      string is str and block_size is a positive integer
                    pad is an empty string or a single character
    ---------------------------------------------------
    """
    assert type(string) == str, 'invalid string'
    assert type(block_size) == int and block_size > 0, 'invalid block size'
    assert type(pad) == str and (pad == '' or len(pad) == 1), 'invalid pad'
    
    s = string
    b = block_size
    blocks = [s[i*b:(i+1)*b] for i in range(ceil(len(s)/b))]
    
    if pad != '':
        if (len(blocks) == 1 and len(blocks[0]) < b) or \
            len(blocks) > 1 and len(blocks[-1]) < len(blocks[0]):
                blocks[-1] += pad*(b - len(blocks[-1]))
    
    return blocks

def restore_text(text, char_indexes):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  char_indexes (list): [[char1,index1],[char2,index2],...]]
    Return:       updated_text (str)
    Description:  Inserts all characters in the char_indexes 2D list (generated by get_char_indexes)
                  into their respective locations
                  Assumes a valid char_indexes 2d list is given
    Asserts:      text is a string and char_indexes is a list
    ---------------------------------------------------
    """
    assert type(text) == str and type(char_indexes) == list, 'invalid input'
    updated_text = text
    for item in char_indexes:
        updated_text = updated_text[:item[1]]+ item[0] + updated_text[item[1]:]
    return updated_text

'______________________________________________________________________________'

def file_to_text(filename):
    """
    ----------------------------------------------------
    Parameters:   filename (str)
    Return:       contents (str)
    Description:  Utility function to read contents of a file
                  Can be used to read plaintext or ciphertext
    Asserts:      filename is a valid name
    ---------------------------------------------------
    """
    assert is_valid_filename(filename), 'invalid filename'
    infile = open(filename,'r')
    contents = infile.read()
    infile.close()
    return contents

'______________________________________________________________________________'

def text_to_file(text, filename):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  filename (str)            
    Return:       no returns
    Description:  Utility function to write any given text to a file
                  If file already exist, previous contents will be erased
    Asserts:      text is a string and filename is a valid filename
    ---------------------------------------------------
    """
    assert type(text) == str , 'invalid text'
    assert is_valid_filename(filename), 'invalid filename'
    outfile = open(filename,'w')
    outfile.write(text)
    outfile.close()
    return