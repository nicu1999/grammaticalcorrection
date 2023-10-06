import sys

def read_n_lines(file_path, n):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = []
        for i in range(n):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
    return lines


def main():
    file_path = sys.argv[1]
    n = int(sys.argv[2])

    lines = read_n_lines(file_path, 2*n)
    for line in lines:
        print(line)

# Print the first n pair of lines

if __name__ == '__main__':
    main()