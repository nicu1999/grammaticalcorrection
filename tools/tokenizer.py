from transformers import  AutoTokenizer

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base', model_max_length=512)

# Add custom tokens in the format <extra_id_i>, where i ranges from 0 to 99
custom_tokens = [f"<extra_id_{i}>" for i in range(100)]
tokenizer.add_tokens(custom_tokens)

# Display the added custom tokens and their corresponding IDs
for token in custom_tokens:
    token_id = tokenizer.convert_tokens_to_ids(token)
    print(f"The ID assigned to the custom token '{token}' is: {token_id}")

# Your text with the custom token and spaces
text = "This is a sentence. <extra_id_0> This is another sentence."

# Tokenize the text
id_vector = tokenizer.encode(text)
# 0 is <s> and 2 is </s>
ids_correct = [0, 192219, 86839, 8, 10, 85292, 85648, 828, 3865, 8425, 48806, 4, 517, 315, 531, 18440, 107, 8951, 451, 346, 22, 165897, 60867, 13, 4, 1011, 1540, 809, 6835, 451, 11090, 314, 66851, 10095, 1362, 1003, 14211, 232168, 13, 4, 2448, 6049, 123583, 133, 53368, 314, 8425, 48806, 321, 22, 165897, 60867, 13, 5, 2]
ids_wrong =[0, 192219, 86839, 27555, 10, 85292, 85648, 828, 3865, 8425, 48806, 4, 517, 315, 531, 18440, 107, 8951, 451, 346, 22, 165897, 60867, 13, 4, 1011, 1540, 809, 6835, 451, 11090, 314, 66851, 10095, 1362, 1003, 14211, 232168, 13, 4, 2448, 6049, 72260, 53368, 404, 8425, 48806, 321, 22, 165897, 60867, 13, 5, 2]
buckets = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
    print(str(buckets[i_b]) + " " +  tokenizer.decode(ids_correct[i_c]))
    i_c += 1
   else:
    if contiguous_3 == True:
        ids_done.append(base_extra_id_token)
        base_extra_id_token += 1
        ids_list_to_replace.append(curent_ids_to_replace)
        curent_ids_to_replace = []
    contiguous_3 = False

   i_b += 1

print(buckets)

print(ids_done)
print(ids_list_to_replace)

for ids in ids_list_to_replace:
   print(tokenizer.decode(ids))

print(tokenizer.decode(ids_correct))
print(tokenizer.decode(ids_done))
print(tokenizer.decode(ids_wrong))

#print(tokenizer.decode([8, 34796]))