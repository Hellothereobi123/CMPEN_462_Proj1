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
    downconverted_list = np.zeros(len(amp_list), dtype=np.complex128)
    I = np.zeros(len(amp_list)) #initializes sin array
    Q = np.zeros(len(amp_list))
    for i in range(len(downconverted_list)): #multiplies the input signal by the sin and cos of the carrier frequency to get the downconverted signal
        curr_I = amp_list[i]*math.cos(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
        curr_Q = amp_list[i]*math.sin(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
        I[i] = curr_I
        Q[i] = curr_Q
        #downconverted_list[i] = complex(curr_I, curr_Q)
    return I, Q
def calc_ifft(mat_size, sample_size): #generates the mat_sizexmat_size FFT matrix for size mat_size
    fft_mat = np.zeros((mat_size, mat_size), dtype=np.complex128)
    for row in range(mat_size):
        for col in range(mat_size):
            fft_mat[row][col] = math.e**complex(0, math.pi*2*(row*col)/mat_size)
    return fft_mat/sample_size
def filter(downconverted_list, sampling_freq, input_size):
    for i in range(len(downconverted_list)):
        if i*sampling_freq/input_size > 5.1 and i*sampling_freq/input_size <= sampling_freq/2:
            print("eeeee")
            downconverted_list[i] = 0
        elif -(input_size-i)*sampling_freq/input_size < -5.1 and -(input_size-i)*sampling_freq/input_size > -sampling_freq/2:
            downconverted_list[i] = 0
    return downconverted_list
def downsample(filtered_I, downsample_factor):
    downsampled_list = np.zeros(len(filtered_I)//downsample_factor)
    for i in range(0, len(downsampled_list), 1):
        downsampled_list[i] = filtered_I[i*downsample_factor]
    return downsampled_list
def correlate(preamble, bigger_list):
    corr_index = 0
    for i in range(len(bigger_list)-len(preamble)):
        corr += preamble[i]*bigger_list[i]
    return corr
filepath = "./input.txt"
carrier_freq = 20 #carrier frequency in hertz
sampling_frequency = 100 #sampling frequency in hertz
input_size = 3000

amp_list = file_read(filepath) #get the list of amplitudes from the file
I, Q = downconversion(amp_list, carrier_freq, sampling_frequency) #gets the downconverted I and Q lists (needed for demodulation)
idft_mat = calc_ifft(input_size, input_size) #calculates the IFFT matrix for the input size (frequency domain to time domain)
dft = (input_size*idft_mat).conjugate().T 
#filter+downsample for I
freq_domain = np.matmul(dft, I) #multiplies the FFT matrix by the filtered downconverted signal I to get the frequency domain representation of the signal
filtered_freq = filter(freq_domain, sampling_frequency, input_size)
time_domain = np.matmul(idft_mat, filtered_freq) #multiplies the IFFT matrix by the filtered frequency domain signal to get the time domain representation of the signal
downsampled_I = downsample(time_domain, 10)
#filter+downsample for Q
freq_domain = np.matmul(dft, Q) #multiplies the FFT matrix by the filtered downconverted signal I to get the frequency domain representation of the signal
filtered_freq = filter(freq_domain, sampling_frequency, input_size)
time_domain = np.matmul(idft_mat, filtered_freq) #multiplies the IFFT matrix by the filtered frequency domain signal to get the time domain representation of the signal
downsampled_Q = downsample(time_domain, 10)

print(downsampled_I)
print(downsampled_Q)


