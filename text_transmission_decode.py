def file_read(file_path): #reads the file of inputs and returns the values as a list of amplitudes
    content = []
    with open(file_path, 'r') as file:
        content = file.read().split("\n")
        content = content[:-1]
    for i in range(len(content)):
        content[i] = float(content[i])
    #print(content)
    return content
def downconversion(amp_list):
    sinlist = [0]*len(amp_list)
    for i in range(len(sinlist))
    cosval = 0
    return sinval, cosval
filepath = "./input.txt"
amp_list = file_read(filepath) #get the list of amplitudes from the file

