import math
from operator import*
#######################CONSTANTS##########################################
#Initial Hash Values:
 
#initial_values = list({'01101010000010011110011001100111', '10111011011001111010111010000101', '00111100011011101111001101110010', '10100101010011111111010100111010', '01010001000011100101001001111111', '10011011000001010110100010001100', '00011111100000111101100110101011', '01011011111000001100110100011001'})

#64 constants 
constants_long = '01000010100010100010111110011000011100010011011101000100100100011011010111000000111110111100111111101001101101011101101110100101001110010101011011000010010110110101100111110001000100011111000110010010001111111000001010100100101010110001110001011110110101011101100000000111101010101001100000010010100000110101101100000001001001000011000110000101101111100101010100001100011111011100001101110010101111100101110101110100100000001101111010110001111111101001101111011100000001101010011111000001100110111111000101110100111001001001101101101001110000011110111110111110010001111000011000001111110000011001110111000110001001000000110010100001110011000010110111101001001011000110111101001010011101001000010010101010010111001011000010101001110111000111011011111001100010001101101010011000001111100101000101010010101010000011000111000110011011011011000000000011001001111100100010111111010110010111111111000111110001101110000000001011111100111101010110100111100100010100011100000110110010100110001101010001000101000010100100101001011001110010011110110111000010101000010100101110000110110010000100111000010011010010110001101101111111000101001100111000000011010001001101100101000010100111001101010100011101100110101000001010101110111000000111000010110010010010111010010010011100100010110010000101101000101011111111101000101000011010100000011010011001100100101111000010010010111000101101110000110001110110110001010001101000111101000110010010111010000001100111010110100110010000011000100100111101000000111000110101100001010001000001101010101000000111000000011001101001001100000100010110000111100011011101101100000010000010011101001000011101110100110000110100101100001011110010110101001110010001110000001100101100110100111011011000101010100100101001011011100111001100101001001111011010000010111001101111111100110111010010001111100000101110111001111000101001010110001101101111100001001100100001111000000101001000110011000111000000100000100010010000101111101111111111111010101001000101000001101100111010111011111011111001101000111111011111000110011100010111100011110010'


constants = {}

####################################BUILD MESSAGE#####################################################
def string_to_binary(input_string):
    binary_string = ''.join(format(ord(char), '08b') for char in input_string)
    return binary_string

def pad_end(binary_string, length):
    return binary_string.ljust(length, '0')

def pad_start(binary_string, length):
    return binary_string.rjust(length, '0')

  
def hash_pad(binary_string):
    binary_string +=('1') #separator
    length = len(binary_string)
    to_multiple = 0 if length % 512 == 0 else 512 - length % 512  #number of zeros needed to reach a multiple of 512
    attach_length = pad_end(binary_string, length + to_multiple - 64)
    return attach_length + pad_start("{0:b}".format(length - 1), 64)

def padAt(myString, num, character, index) -> str: #myString is the string to append, num is the desired final length of the string, character is the character to pad with.
  if(len(myString) > num):
    return myString

  return myString[0: index] + ((num - len(myString)) * character) + myString[index:]

#def bin(s):
        #return str(s) if s<=1 else bin(s>>1) + str(s&1)



        ################################CREATE BLOCKS#################################################################
def split_string(string, length):
    return [string[i:i+length] for i in range(0, len(string), length)]

def create_blocks(full_message):
   return split_string(full_message, 512)
########################################CREATE WORDS#################################################################
def rotation(binary_message, num): # use a negative num for right rot. and positive for left rot.
    return binary_message[num:] + binary_message[:num]

def right_shift(binary_message, num): 
   final_length = len(binary_message)
   new_string = pad_start(binary_message,  num + final_length)
   return new_string[0:final_length]
   
def left_shift(binary_message, num): #string to be shifted, number of shifts
   final_length = len(binary_message)
   new_string = pad_end(binary_message,  num + final_length)
   return new_string[-final_length:]

def sig_zero(binary_message):
   x = rotation(binary_message, -7)
   y = rotation(binary_message, -18)
   z = right_shift(binary_message, 3)
   return xor(xor(y, z), x)

def sig_one(binary_message):
   x = rotation(binary_message, -17)
   y = rotation(binary_message, -19)
   z = right_shift(binary_message, 10)
   return xor(xor(x, y), z)

def big_sig_zero(binary_message):
   x = rotation(binary_message, -2)
   y = rotation(binary_message, -13)
   z = rotation(binary_message, -22)
   return xor(xor(y, z), x)

def big_sig_one(binary_message):
   x = rotation(binary_message, -6)
   y = rotation(binary_message, -11)
   z = rotation(binary_message, -25)
   return xor(xor(x, y), z)

def combine_binary( a: str, b: str) -> str:
        res = ""
        i, j, carry = len(a) - 1, len(b) - 1, 0
        while i >= 0 or j >= 0:
            sum = carry
            if i >= 0 : sum += ord(a[i]) - ord('0') # ord is use to get value of ASCII character
            if j >= 0 : sum += ord(b[j]) - ord('0')
            i, j = i - 1, j - 1
            carry = 1 if sum > 1 else 0
            res += str(sum % 2)
        return res[::-1]
'''
def combine_binary(a: str, b: str) -> str:
   

    binary_sum = str(bin(add(int(a,2),int(b,2))))
    binary_sum = binary_sum[2:]
   
    if(len(binary_sum) > 32):
        binary_sum = binary_sum[len(binary_sum) - 32:]
    return pad_start(binary_sum, 32)
'''
def combine_all(*args):
    num = '0'
    for el in args:
        num = combine_binary(num, el)
    return num

def xor_all(*args):
    num = '0'
    for el in args:
        num = xor(num, el)
    return num
def create_words(block):
   words = split_string(block, 32)
   index = len(words)
   
   while index < 64:
       words.append(combine_all(sig_one(words[index - 2]), words[index - 7], sig_zero(words[index - 15]), words[index - 16]))
       index += 1
   
   return words
############################COMPRESSION##############################################
def choice(e, f, g):
     output = ''

     for i in range(0, len(e)): 
        if e[i] == '0':
            output += g[i]
        else:
            output += f[i]

     return output
def xor(a, b):
    output = ''
    if len(a) is not len(b):
        return a
    for i in range(0, len(a)):
        a1 = int(a[i])
        b1 = int(b[i])
        if(a1 == b1):
            output += '0'
        else:
            output += '1'
    return output

def majority(e, f, g):
    output = ''

    for i in range(0, len(e)):
        e1 = int(e[i])
        f1 = int(f[i])
        g1 = int(g[i])
        if e1 + f1 + g1 > 1:
            output += '1'
        else:
            output += '0'
    return output

def minority(e, f, g): #exact complement to the majority function
    output = ''

    for i in range(0, len(e)):
        e1 = int(e[i])
        f1 = int(f[i])
        g1 = int(g[i])
        if e1 + f1 + g1 > 1:
            output += '0'
        else:
            output += '1'
    return output

def xnor(a, b): #exact complement of xor
    output = ''
    if len(a) is not len(b):
        return a
    for i in range(0, len(a)):
        a1 = int(a[i])
        b1 = int(b[i])
        if(a1 == b1):
            output += '1'
        else:
            output += '0'
    return output

def compress(words: list, initial_values_long):
    
    '''
    initial_values = ['01101010000010011110011001100111']

    initial_values.append('10111011011001111010111010000101')
    initial_values.append('00111100011011101111001101110010')
    initial_values.append('10100101010011111111010100111010')
    initial_values.append('01010001000011100101001001111111')
    initial_values.append('10011011000001010110100010001100')
    initial_values.append('00011111100000111101100110101011')
    initial_values.append('01011011111000001100110100011001')
    '''
    initial_values = split_string(initial_values_long, 32)
#64 constants 
    constants_long = '01000010100010100010111110011000011100010011011101000100100100011011010111000000111110111100111111101001101101011101101110100101001110010101011011000010010110110101100111110001000100011111000110010010001111111000001010100100101010110001110001011110110101011101100000000111101010101001100000010010100000110101101100000001001001000011000110000101101111100101010100001100011111011100001101110010101111100101110101110100100000001101111010110001111111101001101111011100000001101010011111000001100110111111000101110100111001001001101101101001110000011110111110111110010001111000011000001111110000011001110111000110001001000000110010100001110011000010110111101001001011000110111101001010011101001000010010101010010111001011000010101001110111000111011011111001100010001101101010011000001111100101000101010010101010000011000111000110011011011011000000000011001001111100100010111111010110010111111111000111110001101110000000001011111100111101010110100111100100010100011100000110110010100110001101010001000101000010100100101001011001110010011110110111000010101000010100101110000110110010000100111000010011010010110001101101111111000101001100111000000011010001001101100101000010100111001101010100011101100110101000001010101110111000000111000010110010010010111010010010011100100010110010000101101000101011111111101000101000011010100000011010011001100100101111000010010010111000101101110000110001110110110001010001101000111101000110010010111010000001100111010110100110010000011000100100111101000000111000110101100001010001000001101010101000000111000000011001101001001100000100010110000111100011011101101100000010000010011101001000011101110100110000110100101100001011110010110101001110010001110000001100101100110100111011011000101010100100101001011011100111001100101001001111011010000010111001101111111100110111010010001111100000101110111001111000101001010110001101101111100001001100100001111000000101001000110011000111000000100000100010010000101111101111111111111010101001000101000001101100111010111011111011111001101000111111011111000110011100010111100011110010'

    a = initial_values[0]
    b = initial_values[1]
    c = initial_values[2]
    d = initial_values[3]
    e = initial_values[4]
    f = initial_values[5]
    g = initial_values[6]
    h = initial_values[7]
    

    big_constants = get_constants(constants_long)
    
    for i in range(0, 64):
        
        t1 = combine_all(h, big_sig_one(e), choice(e,f,g), big_constants[i], words[i])
        
        t2 = combine_binary(big_sig_zero(a), majority(a,b,c))
        
        
        h = g
        g = f
        f = e
        e = combine_binary(d, t1)
        d = c 
        c = b
        b = a
        a = combine_binary(t1, t2)

    a = combine_binary(a, initial_values[0])
    b = combine_binary(b, initial_values[1])
    c = combine_binary(c, initial_values[2])
    d = combine_binary(d, initial_values[3])
    e = combine_binary(e, initial_values[4])
    f = combine_binary(f, initial_values[5])
    g = combine_binary(g, initial_values[6])
    h = combine_binary(h, initial_values[7])

    return a + b + c + d + e + f + g + h



def sha256(input_string):
    initial_root = '0110101000001001111001100110011110111011011001111010111010000101001111000110111011110011011100101010010101001111111101010011101001010001000011100101001001111111100110110000010101101000100011000001111110000011110110011010101101011011111000001100110100011001'
    binary = string_to_binary(input_string)
    full_message = hash_pad(binary)
    blocks = create_blocks(full_message)
    for block in blocks:
        words = create_words(block)
        initial_root = compress(words, initial_root)
    return bin_to_hex(initial_root)

    
###########################OTHER HELPFUL FUNCTIONS####################################

def bin_to_hex(binary_message): #binary to hex, excludes the 0x at the beginning
    return hex(int(binary_message, 2))[2:]

def get_constants(constants_l): #converting from long-form constant string to list of constants
    return split_string(constants_l, 32)

def print_hexes(binary_list): #accepts a list of binary strings and prints their equivalent hex values
        for i in range(0, 64):
            print(bin_to_hex(binary_list[i]))
            
    
###########################################TEST##################################################

e = '1100'
f = '0010'
g = '1111'

my_input = input("Enter the string to go through SHA-256:")
print("SHA-256 hash:", sha256(my_input))


'''
my_binary = string_to_binary('pizza')

full_message = hash_pad(my_binary)

blocks = create_blocks(full_message)
print(full_message)
create_words(blocks[0])
print(combine_binary(combine_binary(x, y), z))
print(combine_binary(combine_binary(x, z), y))
print(combine_binary(combine_binary(y, z), x))
'''


