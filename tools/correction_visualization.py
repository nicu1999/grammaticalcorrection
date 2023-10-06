import json
from transformers import  AutoTokenizer

def read_n_lines(file_path, n):
    with open(file_path, 'r') as file:
        lines = []
        for i in range(n):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
    return lines

# Visualizes the necessary corrections to transform an incorrect sentence into its corrected version.
# Used for checking if the add/mod/del opperations were extracted successfully

def main():
    file_path = 'licenta\\10_mil_buckets.txt'
    n = 20  # Change this to the number of lines you want to read

    tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base', model_max_length=128)
    custom_tokens = ["<dif>", "</dif>", "<del>", "</del>", "<add>", "</add>"]
    tokenizer.add_tokens(custom_tokens)

    for token in custom_tokens: 
        token_id = tokenizer.convert_tokens_to_ids(token)
        print(f"The ID assigned to the custom token '{token}' is: {token_id}")

    # 0 nothing, 1 dif, 2 del, 3 add
    lines = read_n_lines(file_path, n)
    for line in lines:
        json_data = json.loads(line)
        i_c = 0
        i_w = 0
        i_t = 0 #tags

        correct = []
        wrong = []

        while i_t != len(json_data["labels"]):
            if json_data["labels"][i_t] == 0:
                correct.append(json_data["input_ids_correct"][i_c])
                wrong.append(json_data["input_ids_wrong"][i_w])
                i_c += 1
                i_w += 1

            if json_data["labels"][i_t] == 1:
                correct.append(250002)
                correct.append(json_data["input_ids_correct"][i_c])
                correct.append(250003)
                wrong.append(250002)
                wrong.append(json_data["input_ids_wrong"][i_w])
                wrong.append(250003)
                i_c += 1
                i_w += 1
        
            if json_data["labels"][i_t] == 2:
                wrong.append(250004)
                wrong.append(json_data["input_ids_wrong"][i_w])
                wrong.append(250005)
                i_w += 1

            if json_data["labels"][i_t] == 3:
                correct.append(250006)
                correct.append(json_data["input_ids_correct"][i_c])
                correct.append(250007)
                i_c += 1
                
            i_t += 1

        print(tokenizer.decode(correct))
        print(tokenizer.decode(wrong))
        print()
            
if __name__ == '__main__':
    main()