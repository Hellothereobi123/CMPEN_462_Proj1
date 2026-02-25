def file_read_complex(file_path): #reads the file of inputs and returns the values as a list of amplitudes
    content = []
    with open(file_path, 'r') as file:
        content = file.read().split("\n") 
        content = content[:-1]
    for i in range(len(content)):
        content[i] = complex(content[i][:-1]+"j")
    #print(content)
    return content
print(file_read("./preamble.txt")[0])
