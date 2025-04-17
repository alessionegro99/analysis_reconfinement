from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/transition/" + sys.argv[1]

for filename in os.listdir(path + '/roughdata/'):
    with open(path + '/roughdata/' + filename, 'r') as fp:
        lines = fp.readlines()
    with open(path + '/data/' + filename, 'w') as fp:
        for number, line in enumerate(lines):
            if number > int(sys.argv[2]):
                fp.write(line)

file_list = [file for file in os.listdir(path + "/data/")]

file_groups = {}

for file_name in file_list:
    file_prefix = file_name.split("_")[1]
    if file_prefix not in file_groups:
        file_groups[file_prefix] = []
    file_groups[file_prefix].append(file_name)

for file_prefix, file_group in file_groups.items():
    output_file = f"{path}/data/dati_{file_prefix}"
    with open(output_file, "w") as outfile:
        for i in range(len(file_group)):
            file_group[i] = path + "/data/" + file_group[i]
        for line in fileinput.input(file_group):
            outfile.write(line)

for files in file_list:
    os.remove(path + "/data/" + files)

for filename in os.listdir(path + "/data/"):
    os.rename(path + "/data/" + filename, path + "/data/" + filename + ".dat")