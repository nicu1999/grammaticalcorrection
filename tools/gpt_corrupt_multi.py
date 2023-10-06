import openai
import random
from openai_multi_client import OpenAIMultiOrderedClient, Payload

#
# GT3.5 CAN GENERATE LINE BREAKS NOT ONLY NEWLINWS
#
# Used for generating corrupted sentences in parallel and in Romanian.
# In 20% of cases there are no changes made, in 60% of cases the model
# is prompted to generate only one error and the rest of 20% of cases
# the model is prompted to generate multiple errors 
# Uses the gpt-3.5 api

def dequotetify(original, corrupted):
    if not original or not corrupted:  # check for empty strings
        return corrupted

    original_list = list(original)
    corrupted_list = list(corrupted)

    # If the original phrase doesn't start with a quote but the corrected one does,
    # remove the starting quote from the corrected.
    if original_list[0] != '"' and (corrupted_list[0] == '"' or corrupted_list[0] == '\''):
        corrupted_list.pop(0)


    # If the original phrase doesn't end with a quote but the corrected one does,
    # remove the ending quote from the corrected.
    if original_list[-1] != '"' and (corrupted_list[-1] == '"' or corrupted_list[-1] == '\''):
        corrupted_list.pop(-1)

    return ''.join(corrupted_list)

def trim(s):
    s = s.replace("\n", "")
    s += '\n'
    return s

def on_result(result: Payload):
    to_corrupt = result.metadata['to_corrupt']
    response = result.response['choices'][0]['message']['content']   
    response = response.replace("\n", "")
    response = dequotetify(to_corrupt, response)
    to_corrupt = trim(to_corrupt)
    response = trim(response)
    output_file.write(to_corrupt)
    output_file.write(response)

def make_request(to_corrupt, mode):
    if mode == "single":
        api.request(data={
            "messages":[
                {"role": "system", "content": "Esti un sistem REALISTIC de corupere al frazelor in limba romana. Scopul tau este sa produci greseli gramaticale plauzibile."},
                {"role": "user", "content": f"Creeaza O SINGURA greseala gramaticala sau ortografica pentru urmatoarea fraza. NU OFERI NICIO EXPLICAȚIE!!!\n\nText introdus: \"{to_corrupt}\"\nText corupt:"}
            ]
        }, metadata={'to_corrupt': to_corrupt}, callback=on_result)
    
    if mode == "multiple":
        api.request(data={
            "messages":[
                {"role": "system", "content": "Esti un sistem REALISTSIC de corupere al frazelor in limba romana. Scopul tau este sa produci greseli gramaticale plauzibile."},
                {"role": "user", "content": f"Creeaza MULTIPLE greseli gramaticale sau ortografice pentru urmatoarea fraza. NU OFERI NICIO EXPLICAȚIE!!!\n\nText introdus: \"{to_corrupt}\"\nText corupt:"}
            ]
        }, metadata={'to_corrupt': to_corrupt}, callback=on_result)

def make_requests():
    for i in range(n//8):
        print(i)
        line = file.readline()
        line = trim(line)
        output_file.write(line)
        output_file.write(line)

    for i in range(n//8, (4*n)//5):
        print(i)
        line = file.readline()
        line = line.replace("\n", "")
        #print(line)
        make_request(line, "single")

    for i in range((4*n)//5, n):
        print(i)
        line = file.readline()
        line = line.replace("\n", "")
        #print(line)
        make_request(line, "multiple")

# Replace 'your_api_key_here' with your actual API key
api_key = "api-key"

# Set up the API client with your API key
openai.api_key = api_key

api = OpenAIMultiOrderedClient(endpoint="chats", concurrency=50, data_template={"model": "gpt-3.5-turbo"})

n = 90000

in_file = '../corpus/clean/wiki_clean_split_9990000_2_split_90000_1'
out_file = '../corpus/corrupted/wiki_dirty_gpt_90000.txt'

with open(in_file, 'r', encoding='utf-8') as file:
    with open(out_file, 'w', encoding='utf-8') as output_file:
        api.run_request_function(make_requests)
        api.pull_all()
