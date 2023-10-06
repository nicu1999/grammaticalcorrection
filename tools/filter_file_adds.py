import json

max_input_len = 128
new_file = "add_dataset_128.txt"

#Filter add files so that the number of tags/tokens is under max_input_len

with open('C:\\Users\\Nicu\\Documents\\coding\\corpus\\add_dataset.txt', "r") as f, open(new_file, "w") as g:
    lines = 0
    for line in f:
        data = json.loads(line)
        input_ids = data["input_ids"]
        if len(input_ids) <= max_input_len:
            g.write(line)
            lines += 1

print(f"Wrote {lines} lines to {new_file}.")
