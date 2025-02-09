from sdes import SBOX, SDES
from utilities import file_to_text

def test_SDES_Util():
    print('{}'.format('-'*40))
    print("Start of SDES Utilities Testing")
    print()

    print('Testing is_prime:')
    nums = [97,479,1044,10554571,0,-17]
    for num in nums:
        print(f'is_prime({num}) = {SDES.is_prime(num)}')
    print()

    print('Testing gcd:')
    a = [629,440,-30,540,711,0,[9]]
    b = [357,700,700,539,0,311,27]
    for i in range(len(a)):
        print(f'gcd({a[i]},{b[i]}) = {SDES.gcd(a[i],b[i])}')
    print()

    print('Testing is_relatively_prime:')
    a = [4,540,18,0,[1]]
    b = [5,539,26,26,26]
    for i in range(len(a)):
        print(f'is_relatively_prime({a[i]},{b[i]}) = {SDES.is_relatively_prime(a[i],b[i])}')
    print()
    
    print('Testing Blum Blum Shub: ')    
    p = [383,11,27691, 383,383,384]
    q = [503,19,11, 503,503.0,503]
    bits = [8,4,16, 0,1,1]
    for i in range(len(p)):
        output = SDES.BBS(p[i],q[i],bits[i],'primes.txt')
        print('SDES.BBS({},{},{}) = {}'.format(p[i],q[i],bits[i],output))
    print()

    print('End of SDES Utilities Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_sbox():
    print('{}'.format('-'*40))
    print("Start of SBOX class testing")
    print()
    
    print('Testing SBOX1')
    box1 = [['101','010','001','110','011','100','111','000'],
            ['001','100','110','010','000','111','101','011']]
    sbox1 = SBOX(box1)
    print(sbox1)
    nums = ['1101','0010','0111','0000','010',1010]
    for num in nums:
        print(f'sbox1[{num}] = {sbox1[num]}')
    print()

    print('Testing SBOX2')
    box2 = [['100','000','110','101','111','001','011','010'],
            ['101','011','000','111','110','010','001','100']] 
    sbox2 = SBOX(box2)
    print(sbox2)
    for num in nums:
        print(f'sbox2[{num}] = {sbox2[num]}')
    print()

    print('End of SBOX class Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_sdes_basics():
    print('{}'.format('-'*40))
    print("Start of SDES basics testing")
    print()

    sdes = SDES()
    print('Testing default values (get_value):')   
    cases = ['rounds','key_length','block_size','encoding','sbox1',
             'sbox2','p','q','pad','primes_file','size']
    for c in cases:
        print(f'sdes.get_config_value({c}) = {sdes.get_config_value(c)}')
    print()
    
    print('Testing __str__:')
    print(sdes)
    print()
    
    cases = [['rounds',5],['rounds',1],['rounds',4.3],
             ['p',683],['p',899],
             ['q',684],['q',13.2],
             ['pad','r'],['pad','ab'],['pad',1],['pad','?'],
             ['encoding','B6'],['encoding','ascii'],
             ['block_size',1024],['block_size',243],['block_size',512.0],
             ['key_length',64],
             ['sbox1',[]],
             ['primes_file','primes2.txt']]
    print('Testing set_parameter:')
    for c in cases:
        print(f'sdes.set_parameter({c[0]},{c[1]}) = {sdes.set_parameter(c[0], c[1])}')
    print()
    
    print('Printing SDES object:')
    print(sdes)
    print()

    print('End of SDES basics Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_sdes_keys():
    print('{}'.format('-'*40))
    print("Start of SDES keys testing")
    print()

    print('Testing get_key:')
    sdes = SDES()
    sdes.set_parameter('p',103)
    print('p = {}, q = {}'.format(sdes.get_config_value('p'),sdes.get_config_value('q')))
    print('sdes.get_key() = {}'.format(sdes.get_key()))
    sdes.set_parameter('p',683)
    print('p = {}, q = {}'.format(sdes.get_config_value('p'),sdes.get_config_value('q')))
    print('sdes.get_key() = {}'.format(sdes.get_key()))    
    sdes.set_parameter('q',503)
    print('p = {}, q = {}'.format(sdes.get_config_value('p'),sdes.get_config_value('q')))
    print('sdes.get_key() = {}'.format(sdes.get_key()))        
    print()

    print('Testing get_subkey:')
    print('key = {}'.format(sdes.get_key()))
    for i in range(12):
        print('subkey({}) = {}'.format(i,sdes.get_subkey(i)))
    print()
    
    print('End of SDES keys Testing')
    print('{}'.format('-'*40))
    print()
    return
       
def test_feistel():
    print('{}'.format('-'*40))
    print("Start of Feistel Network testing")
    print()
    
    sdes = SDES()
    
    print('Testing expand:')
    cases = ['011001','00001111','0011','',1011]
    for c in cases:
        print('sdes.expand({}) = {}'.format(c,sdes.expand(c)))
    print()
    
    print('Testing F function:')
    bi = ['111000','100110','10011','100110','100011']
    ki = ['00011010','01100101','01100101','0110010','10111101']
    for i in range(len(bi)):
        print('F({},{}) = {}'.format(bi[i],ki[i],sdes.F(bi[i],ki[i])))
    print()

    print('Testing feistel:')
    bi = ['011100100110','010001100101','01110010011','011100100110']
    ki = ['01100101','11000001','01100101','0110010']
    for i in range(len(bi)):
        print('feistel({},{}) = {}'.format(bi[i],ki[i],sdes.feistel(bi[i],ki[i])))
    print()

    print('End of Feistel Network Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_ECB():
    print('{}'.format('-'*40))
    print("Start of SDES ECB Mode testing")
    print()

    sdes = SDES()
    
    p = [11, 503, 27691, 683, 19, 27691]
    q = [19, 23, 11, 503, 59, 23]
    pads = ['q','x','Q', 'q', '.', 'X']
    rounds = [2,3,4,2,3,2]
    plaintexts = ['OK', 'Sit', 'beet', 'welcome',
                  '"Cryptography" is power', 'go-go']
    for i in range(len(plaintexts)):
        sdes.set_parameter('p', p[i])
        sdes.set_parameter('q', q[i])
        sdes.set_parameter('pad',pads[i])
        sdes.set_parameter('rounds',rounds[i])
        print('key = {}'.format(sdes.get_key()))
        plaintext = plaintexts[i]
        print('plaintext  = {}'.format(plaintext))
        ciphertext = sdes.encrypt(plaintext,'ECB')
        print('ciphertext = {}'.format(ciphertext))
        plaintext2 = sdes.decrypt(ciphertext,'ECB')
        print('plaintext2 = {}'.format(plaintext2))
        print()
        
    print('End of SDES ECB Mode Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_CBC():
    print('{}'.format('-'*40))
    print("Start of SDES CBC Mode testing")
    print()

    sdes = SDES()
    
    p = [11, 43, 27691, 683, 43]
    q = [19, 23, 11, 503, 683]
    plaintexts = ['go', 'CAT', 'seed', 'go-go', 'cryptanalysis tricks']
    for i in range(len(plaintexts)):
        sdes.set_parameter('p', p[i])
        sdes.set_parameter('q', q[i])
        print('key = {}'.format(sdes.get_key()))
        plaintext = plaintexts[i]
        print('plaintext  = {}'.format(plaintext))
        ciphertext = sdes.encrypt(plaintext,'CBC')
        print('ciphertext = {}'.format(ciphertext))
        plaintext2 = sdes.decrypt(ciphertext,'CBC')
        print('plaintext2 = {}'.format(plaintext2))
        print()
        
    print('End of SDES CBC Mode Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_OFB():
    print('{}'.format('-'*40))
    print("Start of SDES OFB Mode testing")
    print()

    sdes = SDES()
    
    p = [11, 43, 27691, 683, 43]
    q = [19, 23, 11, 503, 683]
    plaintexts = ['go', 'CAT', 'seed', 'go-go', 'cryptanalysis tricks']
    for i in range(len(plaintexts)):
        sdes.set_parameter('p', p[i])
        sdes.set_parameter('q', q[i])
        print('key = {}'.format(sdes.get_key()))
        plaintext = plaintexts[i]
        print('plaintext  = {}'.format(plaintext))
        ciphertext = sdes.encrypt(plaintext,'OFB')
        print('ciphertext = {}'.format(ciphertext))
        plaintext2 = sdes.decrypt(ciphertext,'OFB')
        print('plaintext2 = {}'.format(plaintext2))
        print()
        
    print('End of SDES OFB Mode Testing')
    print('{}'.format('-'*40))
    print()
    return

def test_file():
    print('{}'.format('-'*40))
    print("Start of SDES testing over files")
    print()

    sdes = SDES()
    sdes.set_parameter('p', 19)
    sdes.set_parameter('q', 43)
    sdes.set_parameter('rounds',4)
    
    # plaintext = 'It was close upon four before the door opened, and a drunken looking\n'
    # plaintext += 'ill kempt and side flashed with a swallowed face and\n'
    # plaintext += 'disreputable clothes, walked into the room. Used as I was to my\n'
    # plaintext += "friend's splendid powers in the use of disguises, I had to look three\n"
    # plaintext += 'times before I was certain that it was indeed he. With a nod he\n'
    # plaintext += 'vanished into the bedroom, whence he emerged in six minutes\n'
    # plaintext += 'tweed-suited and respectable, as old.'
    
    print('Encryption using ECB:')
    plaintext_ecb = file_to_text('plaintext_ecb.txt')
    print('plaintext:')
    print(plaintext_ecb)
    print()
    ciphertext_ecb = sdes.encrypt(plaintext_ecb, 'ECB')
    print('ciphertext (ECB):')
    print(ciphertext_ecb)
    # text_to_file(ciphertext_ecb, 'ciphertext_ecb.txt')
    print()
    print('Decryption using ECB:')
    ciphertext_ecb = file_to_text('ciphertext_ecb.txt')
    plaintext_ecb2 = sdes.decrypt(ciphertext_ecb, 'ECB')
    print('plaintext (ECB):')
    print(plaintext_ecb2)
    print()

    print('Encryption using CBC:')
    plaintext_cbc = file_to_text('plaintext_cbc.txt')
    print('plaintext:')
    print(plaintext_cbc)
    print()
    ciphertext_cbc = sdes.encrypt(plaintext_cbc, 'CBC')
    print('ciphertext (CBC):')
    print(ciphertext_cbc)
    #text_to_file(ciphertext_cbc, 'ciphertext_cbc.txt')
    print()
    print('Decryption using CBC:')
    ciphertext_cbc = file_to_text('ciphertext_cbc.txt')
    plaintext_cbc2 = sdes.decrypt(ciphertext_cbc, 'CBC')
    print('plaintext (CBC):')
    print(plaintext_cbc2)
    print()

    print('Encryption using OFB:')
    plaintext_ofb = file_to_text('plaintext_ofb.txt')
    print('plaintext:')
    print(plaintext_ofb)
    print()
    ciphertext_ofb = sdes.encrypt(plaintext_ofb, 'OFB')
    print('ciphertext (OFB):')
    print(ciphertext_ofb)
    #text_to_file(ciphertext_ofb, 'ciphertext_ofb.txt')
    print()
    print('Decryption using OFB:')
    ciphertext_ofb = file_to_text('ciphertext_ofb.txt')
    plaintext_ofb2 = sdes.decrypt(ciphertext_ofb, 'OFB')
    print('plaintext (OFB):')
    print(plaintext_ofb2)
    print()
    
    print('End of SDES testing over files')
    print('{}'.format('-'*40))
    print()
    return
  
test_SDES_Util()
test_sbox()
test_sdes_basics()
test_sdes_keys()
test_feistel()
test_ECB()
test_CBC()
test_OFB()
test_file()