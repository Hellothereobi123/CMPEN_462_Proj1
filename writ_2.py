import math
import numpy as np
import scipy.signal as signal
from scipy import fft 
def file_read_complex(file_path): #reads the file of inputs and returns the values as a list of complex amplitudes
    content = []
    with open(file_path, 'r') as file:
        content = file.read().split("\n") 
        content = content[:-1]
    for i in range(len(content)):
        #print(content[i][:-1]+"j")
        content[i] = complex(content[i][:-1]+"j")
    #print(content)
    return content
def merge_bits(bitstream): # merged two 4 bit elements into one 8 bit element
    merged_bitstream  = []
    for i in range(0, len(bitstream)-1, 2):
        new_bits = bitstream[i] << 4
        new_bits = new_bits | bitstream[i+1]
        merged_bitstream.append(new_bits)
    return merged_bitstream
def find_QAM(Q,I): # found 16QAM by determining what binary to assign depending on its Q and I coordinates
    bitstream = []

    for j in range(len(Q)):
        bit_val = 0b0000
        if (Q[j] > 2):
            bit_val = bit_val | 0b0000
        elif (Q[j] <= 2 and Q[j] > 0):
            bit_val = bit_val | 0b0100
        elif (Q[j] <= 0 and Q[j] > -2):
            bit_val = bit_val | 0b1100
        elif (Q[j] < -2):
            bit_val = bit_val | 0b1000

        if (I[j] > 2):
            bit_val = bit_val | 0b0000
        elif (I[j] <= 2 and I[j] > 0):
            bit_val = bit_val | 0b0001
        elif (I[j] <= 0 and I[j] > -2):
            bit_val = bit_val | 0b0011
        elif (I[j] < -2):
            bit_val = bit_val | 0b0010

        bitstream.append(bit_val)

    return bitstream #return an array of 4bit binary derived from the signals 
def binary_to_ascii(bitstream): #converts each 8bit binary into a character 
    ascii_vector = []  
    for i in range(len(bitstream)):
        ascii_vector.append(chr(bitstream[i]%256))
    return ascii_vector
complex_list = np.array(file_read_complex("./writ_h2_data.txt"))
X = fft.fft(complex_list)
print(np.round(X, 2))



bitstream = find_QAM(X.imag, X.real) #assigned each signal a binary QAM value, multiply by 2 becuase it was divided by two when downconverting
ascii_bitsteam = merge_bits(bitstream) # merge two 4 bits into 8 bits 
ascii_vector = binary_to_ascii(ascii_bitsteam) # change 8 bits into ascii 
ascii_string=''.join(ascii_vector) # join the Ascii together to create full sentence 
ascii_string = ascii_string.replace('!', ' ') # remove null characters from the string
print(ascii_string) # print the unchecked out put 