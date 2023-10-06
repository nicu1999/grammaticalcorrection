import json

max_input_len = 128
old_file = '../corpus/results_2/wiki_dirty_gpt_100000_shuffled_inter.txt'
new_file = "../corpus/results_2/wiki_dirty_gpt_100000_shuffled_inter_128.txt"

# Used for filtering MOD/DEL datasets such that the number of tokens/tags
# is under max_input_len

with open(old_file, "r") as f, open(new_file, "w") as g:
    lines = 0
    total_lines = 0

    in_lines = f.readlines()

    i = 0

    while i < len(in_lines):
        total_lines += 2
        data_1 = json.loads(in_lines[i])
        data_2 = json.loads(in_lines[i+1])
        input_ids_1 = data_1["input_ids"]
        input_ids_2 = data_2["input_ids"]

        if (len(input_ids_1) <= max_input_len) and (len(input_ids_2) <= max_input_len):
            g.write(in_lines[i])
            g.write(in_lines[i+1])
            lines += 2
        
        i+=2

print(f"Wrote {lines} lines to {new_file}. Deleted {total_lines - lines}.")
