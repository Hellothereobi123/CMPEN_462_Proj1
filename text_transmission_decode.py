import math
import numpy as np
import scipy.signal as signal
from scipy import fft 
from spellchecker import SpellChecker

#################################################################################################################################################
#helper functions

def file_read(file_path): #reads the file of inputs and returns the values as a list of amplitudes
    content = []
    with open(file_path, 'r') as file:
        content = file.read().split("\n") 
        content = content[:-1]
    for i in range(len(content)):
        content[i] = float(content[i])
    #print(content)
    return content


def file_read_complex(file_path): #reads the file of inputs and returns the values as a list of complex amplitudes
    content = []
    with open(file_path, 'r') as file:
        content = file.read().split("\n") 
        content = content[:-1]
    for i in range(len(content)):
        content[i] = complex(content[i][:-1]+"j")
    #print(content)
    return content


def downconversion(amp_list, carrier_frequency, sampling_frequency):
    downconverted_list = np.zeros(len(amp_list), dtype=np.complex128)
    I = np.zeros(len(amp_list)) #initializes sin array
    Q = np.zeros(len(amp_list))
    for i in range(len(downconverted_list)): #multiplies the input signal by the sin and cos of the carrier frequency to get the downconverted signal
        curr_I = amp_list[i]*math.cos(2*math.pi*carrier_frequency*i*(1/sampling_frequency)) 
        curr_Q = amp_list[i]*math.sin(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
        I[i] = curr_I
        Q[i] = curr_Q
    return I, Q


def filter(downconverted_list, sampling_freq, input_size): #filters the signals by elimating all freq out side of -5.1 to 5.1
    for i in range(len(downconverted_list)):
        if i*sampling_freq/input_size > 5.1 and i*sampling_freq/input_size <= sampling_freq/2:
            downconverted_list[i] = 0
        elif -(input_size-i)*sampling_freq/input_size < -5.1 and -(input_size-i)*sampling_freq/input_size > -sampling_freq/2:
            downconverted_list[i] = 0
    return downconverted_list


def downsample(filtered_I, downsample_factor):  # downsample by only taking every tenth value 
    downsampled_list = np.zeros(len(filtered_I)//downsample_factor, dtype=np.complex128)
    for i in range(0, len(downsampled_list), 1):
        downsampled_list[i] = filtered_I[i*downsample_factor]
    return downsampled_list


def correlate(preamble, bigger_list): #find a the location of the highest correlation with the preamble so we know where to chop off the noise 
    corr_index = 0
    max_corr = 0
    for i in range(len(bigger_list)-len(preamble)):
        corr = signal.correlate(bigger_list[i:i+len(preamble)], preamble, mode='valid')[0]
        if np.abs(corr) > np.abs(max_corr):
            max_corr = corr
            corr_index = i
    return corr_index


def combine_I_Q(I, Q): #combined I and Q in a I+JQ format in order to correlate with preamble 
    combined_list = np.zeros(len(I), dtype=np.complex128)
    for i in range(len(I)):
        combined_list[i] = I[i]+1j*Q[i]
    return combined_list

def remove_preamble_noise(index, preamble_size, Q, I): # removed the noise and preamble from the signals 
    temp_Q = Q[index+preamble_size:]
    temp_I = I[index+preamble_size:]
    return temp_Q, temp_I

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

def merge_bits(bitstream): # merged two 4 bit elements into one 8 bit element
    merged_bitstream  = []
    for i in range(0, len(bitstream)-1, 2):
        new_bits = bitstream[i] << 4
        new_bits = new_bits | bitstream[i+1]
        merged_bitstream.append(new_bits)
    return merged_bitstream

def binary_to_ascii(bitstream): #converts each 8bit binary into a character 
    ascii_vector = []  
    for i in range(len(bitstream)):
        ascii_vector.append(chr(bitstream[i]%256))
    return ascii_vector

def error_checking(str_list): #uses spel check libriary to spell check the words in a list 
    correct_list =[]
    spell = SpellChecker()

    for word in str_list:
        correct_list.append(spell.correction(word)) # corrects word if it knows what it is, if not append none
    return correct_list # returns a list of corrected words 

#############################################################################################################################################
#testing functions begin here 

filepath = "./input.txt"
carrier_freq = 20 #carrier frequency in hertz
sampling_frequency = 100 #sampling frequency in hertz
input_size = 3000 # number of samples 

amp_list = file_read(filepath) #get the list of amplitudes from the file
I, Q = downconversion(amp_list, carrier_freq, sampling_frequency) #gets the downconverted I and Q lists (needed for demodulation)

#filter+downsample for I
freq_domain = fft.fft(I) #multiplies the FFT matrix by the filtered downconverted signal I to get the frequency domain representation of the signal
filtered_freq = filter(freq_domain, sampling_frequency, input_size) #filter the signal 
time_domain = (fft.ifft(filtered_freq)).real #multiplies the IFFT matrix by the filtered frequency domain signal to get the time domain representation of the signal. In addition we mustconvert to real in order to use for QAM
downsampled_I = downsample(time_domain, 10) #downsample I signal 


#filter+downsample for Q
freq_domain = fft.fft(Q) #  #multiplies the FFT matrix by the filtered downconverted signal I to get the frequency domain representation of the signal
filtered_freq = filter(freq_domain, sampling_frequency, input_size) #filter the signal 
time_domain = (fft.ifft(filtered_freq)).real #multiplies the IFFT matrix by the filtered frequency domain signal to get the time domain representation of the signal. In addition we mustconvert to real in order to use for QAM
downsampled_Q = downsample(time_domain, 10) #downsample Q signal

#get preamble list
preamble = file_read_complex("./preamble.txt") 
comb = combine_I_Q(downsampled_I, downsampled_Q) #combine I and Q for correlation
corr_index = correlate(preamble, comb) #find the location of highest correlation 
final_Q, final_I = remove_preamble_noise(corr_index, len(preamble), downsampled_Q, downsampled_I) #remove noise and preamble from I and Q signals

#translating signals into words 
bitstream = find_QAM(final_Q*2, final_I*2) #assigned each signal a binary QAM value, multiply by 2 becuase it was divided by two when downconverting
ascii_bitsteam = merge_bits(bitstream) # merge two 4 bits into 8 bits 
ascii_vector = binary_to_ascii(ascii_bitsteam) # change 8 bits into ascii 
ascii_string=''.join(ascii_vector) # join the Ascii together to create full sentence 
print(ascii_string) # print the unchecked out put 

#below is the word spell checker 
"""
word_str = ascii_string.split()
corrected_str = error_checking(word_str) #spell check every word
print(corrected_str)
print(''.join(corrected_str))
"""






