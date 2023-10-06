import json

# Checks if all of the lines of the mT5 training dataset are homogenous

def check_format(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        for line in f:
            data = json.loads(line)
            if not isinstance(data, dict):
                print(f"Line is not a dictionary: {line}")
                continue
            if not set(data.keys()) == {"input", "output"}:
                print(f"Dictionary keys do not match expected format: {data}")
                continue
            if not isinstance(data["input"], str) or not isinstance(data["output"], str):
                print(f"Input or output are not strings: {data}")
                continue
            if "<extra_id_0>" not in data["input"] or "<extra_id_0>" not in data["output"]:
                print(f"Missing <extra_id_0> in input or output: {data}")

check_format("C:\\Users\\Nicu\\Documents\\coding\\corpus\\mt5_test.txt")