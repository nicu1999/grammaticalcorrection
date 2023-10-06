filename = "../corpus/mt5_training.txt"

# Counts the number of files

with open(filename, "r", encoding='utf8') as f:
    lines = 0
    for line in f:
        lines += 1

print(f"The file {filename} has {lines} lines.")