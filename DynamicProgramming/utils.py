def read_data(file_name):
    """
    Loads data from MatLab format files.
    """
    with open(file_name, 'r') as f:
        line = f.readline()
        network = []
        while line:
            if "nNodes" in line:
                nNodes = int(line.split("=")[1].strip()[:-1])
                line = f.readline()
                continue
            elif "wTime" in line:
                wTime = int(line.split("=")[1].strip()[:-1])
                line = f.readline()
                continue
            elif "wInco" in line:
                wInco = int(line.split("=")[1].strip()[:-1])
                line = f.readline()
                continue
            elif "Network" in line:
                while True:
                    line = f.readline()
                    if "]" in line:
                        line = f.readline()
                        break
                    row = line.strip()[:-1] if ";" in line else line.strip()
                    row = row.split(" ")
                    int_row = []
                    for i in row:
                        try:
                            num = int(i)
                            int_row.append(num)
                        except ValueError:
                            continue
                    network.append(int_row)

    return nNodes, wTime, wInco, network


if __name__ == "__main__":
    nNodes, wTime, wInco, network = read_data("./Network3.m")
    print(nNodes)
    print(wTime)
    print(wInco)
    print(network)
