import Levenshtein
import sys

def levenshtein_percentage(string1, string2):
    lev_distance = Levenshtein.distance(string1, string2)
    max_possible_distance = max(len(string1), len(string2))
    similarity_percentage = ((max_possible_distance - lev_distance) / max_possible_distance) * 100
    return similarity_percentage


def check_lines(lines1, lines2, n, cutoff, skips):
    catches = 0
    for i in range(n):
        similarity = levenshtein_percentage(lines1[i], lines2[i])
        if similarity < cutoff:
            print(similarity)
            print(i)
            print(lines1[i])
            print(lines2[i])
            if catches >= skips: #print skips + 1 lines
                break
            catches += 1

# use python3 fix_pairs.py <cutoff> <skips>
# Used for checking and catching lines that are too disimilar
# (meaning their levenshtein distance score is over the cutoff)
# Uses 2 files for the input

file1_path = '../corpus/results_2/NAC-sentences-human.txt'
file2_path = '../corpus/results_2/NAC-sentences-original.txt'
lines = []
cutoff = int(sys.argv[1])
skips = int(sys.argv[2])
with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
    lines1 = file1.readlines()
    lines2 = file2.readlines()
    print(len(lines1))
    print(len(lines2))
    check_lines(lines1, lines2, 100000, cutoff, skips)
