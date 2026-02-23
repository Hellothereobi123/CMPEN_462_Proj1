import math
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
    sinlist = [0]*len(amp_list)
    coslist = [0]*len(amp_list)
    for i in range(len(sinlist)):
        sinlist[i] = amp_list[i]*math.sin(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
    for i in range(len(sinlist)):
        coslist[i] = amp_list[i]*math.cos(2*math.pi*carrier_frequency*i*(1/sampling_frequency))
    sinlist, coslist

                   
    return sinlist, coslist
filepath = "./input.txt"
carrier_freq = 20 #carrier frequency in hertz
sampling_frequency = 100 #sampling frequency in hertz

amp_list = file_read(filepath) #get the list of amplitudes from the file
sinlist, coslist = downconversion(amp_list, carrier_freq, sampling_frequency) #gets the downconverted sin and cos lists (needed for demodulation)



