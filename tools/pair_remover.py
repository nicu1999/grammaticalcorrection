import Levenshtein
import sys
from pynput.keyboard import Key, Controller

def levenshtein_percentage(string1, string2):
    lev_distance = Levenshtein.distance(string1, string2)
    max_possible_distance = max(len(string1), len(string2))
    similarity_percentage = ((max_possible_distance - lev_distance) / max_possible_distance) * 100
    return similarity_percentage


def fix_lines(lines, cutoff):

    i = 0
    keyboard = Controller()
    while i < len(lines):
        if i%2 == 0:
            similarity = levenshtein_percentage(lines[i], lines[i+1])
            if similarity < cutoff:
                print(i+1)
                print(similarity)
                print(lines[i])
                print(lines[i+1])
                print("Delete pair? y or n:\n")

                if input() == 'y':
                    del lines[i]
                    del lines[i]
                    print("\n")
                    continue
                else:
                    print("\n")
        i += 1
    return lines

# Used for filering/removing a pair of sentences that that are under the cutoff
# Uses the input of the user

file_path = '../corpus/corrupted/wiki_dirty_gpt_90000.txt'
lines = []
cutoff = int(sys.argv[1])
with open(file_path, 'r') as file:
    lines = file.readlines()
    result = fix_lines(lines, cutoff)
    
with open(file_path, 'w') as file:
    for line in result:
        file.write(line)
    file.flush()