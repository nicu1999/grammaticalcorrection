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

# Create training data for the mt5 model

def main():

    with open("../corpus/mt5_training.txt", "w", encoding='utf8') as file:

        tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base', model_max_length=128)

        custom_tokens = [f"<extra_id_{i}>" for i in range(100)]
        tokenizer.add_tokens(custom_tokens)

        for token in custom_tokens:
            token_id = tokenizer.convert_tokens_to_ids(token)
            print(f"The ID assigned to the custom token '{token}' is: {token_id}")

        file_path = '../corpus/10_mil_buckets.txt'
        n = 9944346  # Change this to the number of lines you want to read

        lines = read_n_lines(file_path, n)
        for line in lines:
            json_data = json.loads(line)

            ids_correct = json_data['input_ids_correct']
            buckets = json_data['labels']

            if 3 not in buckets:
                continue

            ids_done = []
            ids_list_to_replace = []
            curent_ids_to_replace = []
            base_extra_id_token = 250002
            i_b = 0
            i_c = 0
            contiguous_3 = False
            while i_b < len(buckets):
                if buckets[i_b] != 2:
                    if buckets[i_b] == 3:
                        contiguous_3 = True
                        curent_ids_to_replace.append(ids_correct[i_c])
                    else:
                        if contiguous_3 == True:
                            ids_done.append(base_extra_id_token)
                            base_extra_id_token += 1
                            ids_list_to_replace.append(curent_ids_to_replace)
                            curent_ids_to_replace = []
                        contiguous_3 = False
                        ids_done.append(ids_correct[i_c])
                    i_c += 1
                else:
                    if contiguous_3 == True:
                        ids_done.append(base_extra_id_token)
                        base_extra_id_token += 1
                        ids_list_to_replace.append(curent_ids_to_replace)
                        curent_ids_to_replace = []
                    contiguous_3 = False

                i_b += 1
            
            ids_done.pop(0)
            ids_done.pop(-1)

            input_str = tokenizer.decode(ids_done)

            x = 250002

            output_list = [x]

            for sublist in ids_list_to_replace:
                output_list.extend(sublist)
                x += 1
                output_list.append(x)
            
            output_str = tokenizer.decode(output_list)
            item = {"input":input_str, "output":output_str}

            json_str = json.dumps(item, ensure_ascii=False)
            file.write(json_str)
            file.write('\n')

if __name__ == '__main__':
    main()