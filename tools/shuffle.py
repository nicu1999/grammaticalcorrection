import random

def zip_lines(lines):
    pairs = []
    i = 0
    while i < len(lines):
        pairs.append([lines[i], lines[i+1]])
        i += 2
    return pairs

def shuffle(pairs):
    random.shuffle(pairs)
    return pairs

def unzip(pairs):
    lines = []
    for i in range(len(pairs)):
        lines.append(pairs[i][0])
        lines.append(pairs[i][1])
    
    return lines

file_path = '../corpus/corrupted/wiki_dirty_gpt_100000.txt'
file_result = '../corpus/corrupted/wiki_dirty_gpt_100000_shuffled.txt'
lines = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    pairs = zip_lines(lines)
    pairs = shuffle(pairs)
    lines = unzip(pairs)

# Randomly shuffle all line pairs within a file
# Used for unbiasing the gpt generated training data
# (In the file, unmodified sentence pairs are listed first, 
# followed by the gpt API calls arriving later.)

with open(file_result, "w") as file:
    for line in lines:
        file.write(line)