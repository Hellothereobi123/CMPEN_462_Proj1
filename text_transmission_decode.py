import math
import numpy as np
def file_read(file_path): #reads the file of inputs and returns the values as a list of amplitudes
    content = []
    with open(file_path, 'r') as file:
        content = file.read().split("\n") 
        content = content[:-1]
    for i in range(len(content)):
        content[i] = float(content[i])
    #print(content)
    return content
def downconversion(amp_list, carrier_frequency, sampling_frequency):
    sinlist = np.zeros(len(amp_list)) #initializes sin array
    coslist = np.zeros(len(amp_list))
    for i in range(len(sinlist)): #multiplies the input signal by the sin and cos of the carrier frequency to get the downconverted signal
        sinlist[i] = amp_list[i]*math.sin(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
    for i in range(len(sinlist)):
        coslist[i] = amp_list[i]*math.cos(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
    return sinlist, coslist
def calc_fft(mat_size): #generates the mat_sizexmat_size FFT matrix for size mat_size
    fft_mat = np.zeros((mat_size, mat_size), dtype=np.complex128)
    for row in range(mat_size):
        for col in range(mat_size):
            fft_mat[row][col] = math.e**complex(0, math.pi*2*(row*col)/mat_size)
    return fft_mat
def filter(downconverted_list):
    for i in range(len(downconverted_list)):
        if downconverted_list[i] < -5.1 or downconverted_list[i] > 5.1:
            #print(downconverted_list[i])
            downconverted_list[i] = 0
    return downconverted_list
filepath = "./input.txt"
carrier_freq = 20 #carrier frequency in hertz
sampling_frequency = 100 #sampling frequency in hertz

amp_list = file_read(filepath) #get the list of amplitudes from the file
sinlist, coslist = downconversion(amp_list, carrier_freq, sampling_frequency) #gets the downconverted sin and cos lists (needed for demodulation)
filtered_sinlist = filter(sinlist)

print(filtered_sinlist)
print(calc_fft(30)[1][1])



