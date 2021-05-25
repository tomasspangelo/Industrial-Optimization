from container import Container


def read_data(filename):
    """
    Reads the data that is needed to solve the problem.
    :param filename: path to the file.
    :return: b: number of bays, s: number of stacks, t: number of tiers, and dictionary
    of Container objects where key=id.
    """
    b = 0
    s = 0
    t = 0

    containers = []
    with open(filename, 'r') as f:
        b = int(f.readline())
        s = int(f.readline())
        t = int(f.readline())

        containers = {}
        c = 1
        line = f.readline()
        while line:
            containers[c] = Container(c, int(line))
            c += 1
            line = f.readline()
        return b, s, t, containers


if __name__ == "__main__":
    b, s, t, containers = read_data("./instance1.txt")
    pass
