f = open("testfile.txt", "rb+")

line = " "
while line != b'':
    line = f.readline()
    print(line)
    if "ich" in line.decode("utf-8"):
        f.seek(-len(line), 1)
        f.write("::".encode("utf-8"))
        break
f.close()