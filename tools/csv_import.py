import csv
from transformers import  AutoTokenizer

max_length = 128

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base', model_max_length=512)

# Import the CSV file and split it into 2 files: 
# the original erroneous sentences and the human corrected version

csv_filename = '../corpus/results_2/W-sentence.csv'
original_filename = '../corpus/results_2/W-sentence-original.txt'
human_filename = '../corpus/results_2/W-sentence-human.txt'


with open(csv_filename, 'r', encoding='utf-8') as csv_file, open(original_filename, 'w', encoding='utf-8') as original_file, open(human_filename, 'w', encoding='utf-8') as human_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    row_limit = 6
    count = 0

    for row in csv_reader:
        tokens_original = tokenizer(row[0])
        tokens_human = tokenizer(row[1])

        if len(tokens_original) <= 128 and len(tokens_human) <= 128:
            if row[0].endswith('\n'):
                original_file.write(row[0])
            else:
                original_file.write(row[0] + '\n')

            if row[1].endswith('\n'):
                human_file.write(row[1])
            else:
                human_file.write(row[1] + '\n')
        count += 1