original = '../corpus/results_2/golden_corpus_128_filtered_well_formed.txt'
corrected_file = '../corpus/results_2/golden_corpus_128_filtered_well_formed_no_duplicates.txt' 

# Used for removing duplicates. Uses a single file.

with open(original, 'r', encoding='utf-8') as ofile:
    with open(corrected_file, 'w', encoding='utf-8') as cfile:
        lines = ofile.readlines()
        i = 0
        while i < len(lines):
            if lines[i] != lines[i+1]:
                cfile.write(lines[i])
                cfile.write(lines[i+1])
            i+=2