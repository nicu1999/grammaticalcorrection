import sys
import os

def split_file(file_path, total_lines, num_files):
    lines_per_split = total_lines // num_files

    with open(file_path, 'r') as file:
        for i in range(num_files):
            split_file_name = f'split_{i+1}_{os.path.basename(file_path)}'
            with open(split_file_name, 'w') as split_file:
                for _ in range(lines_per_split):
                    line = file.readline()
                    if not line:
                        break
                    split_file.write(line)

                # Handling the case when total_lines is not divisible by num_files
                if i == num_files - 1:
                    while True:
                        line = file.readline()
                        if not line:
                            break
                        split_file.write(line)

# Split an input file into <num_files> other files.

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python split_file_evenly.py <input_file> <total_lines> <num_files>")
        sys.exit(1)

    file_path = sys.argv[1]
    total_lines = int(sys.argv[2])
    num_files = int(sys.argv[3])

    if not os.path.isfile(file_path):
        print(f"Error: {file_path} does not exist.")
        sys.exit(1)

    split_file(file_path, total_lines, num_files)