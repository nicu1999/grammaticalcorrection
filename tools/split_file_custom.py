import sys
import os

def split_file(file_path, total_lines, chunk, make_second_file):

    with open(file_path, 'r') as file:
            split_file_name = f'{file_path}_split_{chunk}_1'
            with open(split_file_name, 'w') as split_file:
                for _ in range(chunk):
                    line = file.readline()
                    if not line:
                        break
                    split_file.write(line)

            if make_second_file:
                split_file_name = f'{file_path}_split_{total_lines - chunk}_2'
                with open(split_file_name, 'w') as split_file:
                    for _ in range(total_lines - chunk):
                        line = file.readline()
                        if not line:
                            break
                        split_file.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python split_file_custom.py <input_file> <total_lines> <first_chunk> <make_second_file>\n This will take a chunk of the file, and OPTIONALLY make a second file with the chunk missing. Use True or False as argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    total_lines = int(sys.argv[2])
    chunk = int(sys.argv[3])
    make_second_file = sys.argv[4] == "True"

    if not os.path.isfile(file_path):
        print(f"Error: {file_path} does not exist.")
        sys.exit(1)

    split_file(file_path, total_lines, chunk, make_second_file)