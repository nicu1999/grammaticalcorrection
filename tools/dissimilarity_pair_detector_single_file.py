import Levenshtein
import sys

def levenshtein_percentage(string1, string2):
    lev_distance = Levenshtein.distance(string1, string2)
    max_possible_distance = max(len(string1), len(string2))
    similarity_percentage = ((max_possible_distance - lev_distance) / max_possible_distance) * 100
    return similarity_percentage


def fix_lines(lines, n, cutoff, skips):
    catches = 0
    for i in range(2*n):
        #print(lines[i])
        if i%2 == 0:
            similarity = levenshtein_percentage(lines[i], lines[i+1])
            if similarity < cutoff:
                print(similarity)
                print(i+1)
                print(lines[i])
                print(lines[i+1])
                if catches >= skips: #printeaza skips + 1 linii
                    break
                catches += 1

#use python3 fix_pairs.py <file_path> <cutoff> <skips>
# Used for checking and catching lines that are too disimilar
# (meaning their levenshtein distance score is over the cutoff)
# Uses 1 files for the input

file_path = int(sys.argv[1])
lines = []
cutoff = int(sys.argv[2])
skips = int(sys.argv[3])
with open(file_path, 'r') as file:
    lines = file.readlines()
    print(len(lines))
    fix_lines(lines, 100000, cutoff, skips)
