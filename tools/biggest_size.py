import json

max_len = 0

# Checks each line of the inter data files to check the largest number
# of input ids. Used in determining the optimal input size for our
# models such that we keep a balance between performance and training
# time 

with open("../corpus/golden_corpus_inter.txt", "r") as f:
    for line in f:
        data = json.loads(line)
        input_ids = data["input_ids"]
        if len(input_ids) > max_len:
            max_len = len(input_ids)
            print(f"New maximum length found: {max_len}")