from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + sys.argv[1] 

therm = int(sys.argv[2]) # number of configurations to be discarded

for filename in os.listdir(path + '/roughdata/'): # thermalization removal
    with open(path + '/roughdata/' + filename, 'r') as fp:
        lines = fp.readlines()
    with open(path + '/data/' + filename, 'w') as fp:
        for number, line in enumerate(lines):
            if number > therm:
                fp.write(line)

file_list = [file for file in os.listdir(path + '/data/')] 
for i in range(len(file_list)):
    file_list[i] = path + "/data/" + file_list[i]

with open(path + "/data/dati.dat", "w") as outfile: # writing of a new datafile, merging all of the other datafiles with their thermalization removed
    for f in file_list:
        with open(f, "r") as infile:
            outfile.write(infile.read())

for files in file_list:
    os.remove(files)