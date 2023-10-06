# Merge/zip 2 file togheter

file_path_1 = '../corpus/corrupted/wiki_dirty_gpt_10000.txt'
file_path_2 = '../corpus/corrupted/wiki_dirty_gpt_90000.txt'
file_path_final = '../corpus/corrupted/wiki_dirty_gpt_100000.txt'
lines_final = []
with open(file_path_1, 'r') as file_1:
    with open(file_path_2, 'r') as file_2:
        lines_1 = file_1.readlines()
        lines_2 = file_2.readlines()
        lines_final = lines_1 + lines_2

        with open(file_path_final, 'w') as file:
            for line in lines_final:
                file.write(line)
            file.flush()

    