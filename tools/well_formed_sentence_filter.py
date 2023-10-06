# Define input and output file names
input_filename = "../corpus/results_2/golden_corpus_128_filtered.txt"
output_filename_1 = "../corpus/results_2/golden_corpus_128_filtered_well_formed.txt"
import regex as re

def is_well_formed(text):
    return re.match('^[A-Z][^?!.]*[?.!]$', text) is not None

# Function to check if a text is well-formed
# Well-formed text should start with a capital letter, not contain multiple sentences, and end with a punctuation mark

# Open both files
with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename_1, 'w', encoding='utf-8') as outfile1:
    # Enumerate through lines in input file (line numbers start from 0)
    lines = infile.readlines()
    i = 0
    while i < len(lines):
        if(is_well_formed(lines[i])):
            outfile1.write(lines[i])
            outfile1.write(lines[i+1])
        i+=2