# Define input and output file names
input_filename = "../corpus/results_2/golden_corpus_128_filtered_well_formed_no_duplicates.txt"
output_filename_1 = "../corpus/results_2/golden_corpus_128_filtered_well_formed_no_duplicates_human.txt"
output_filename_2 = "../corpus/results_2/golden_corpus_128_filtered_well_formed_no_duplicates_original.txt"

# Used to split the golden corpus into the original sentences and the human corrected sentences.
# Open both files
with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename_1, 'w', encoding='utf-8') as outfile1, open(output_filename_2, 'w', encoding='utf-8') as outfile2:
    # Enumerate through lines in input file (line numbers start from 0)
    for i, line in enumerate(infile):
        # If line number is even, write line to output file
        if i % 2 == 0:
            outfile1.write(line)
        else:
            outfile2.write(line)