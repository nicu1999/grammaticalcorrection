import openai
import random

# Used for generating corrupted sentences in Romanian.
# Uses the gpt-3.5 api

# Replace 'your_api_key_here' with your actual API key
api_key = "api-key"

# Set up the API client with your API key
openai.api_key = api_key

def generate_text(to_correct):
    choice = random.choices([0, 1, 2], weights=[0.2, 0.6, 0.2], cum_weights=None, k=1)
    choice = choice[0]
    print(choice)
    choices = ["",
               f"Creeaza o singura greseala gramaticala sau ortografica pentru urmatoarea fraza. NU OFERI NICIO EXPLICAȚIE!!!\n\nText introdus: \"{to_correct}\"\nText corupt:",
               f"Creeaza una sau RAREORI mai multe greseli gramticale sau ortografice pentru urmatoarea fraza. NU OFERI NICIO EXPLICAȚIE!!!\n\nText introdus: \"{to_correct}\"\nText corupt:"]
    
    message_content = choices[choice]
    
    if choice == 0:
        return to_correct

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #temperature=0,
        #presence_penalty=-1,
        #frequency_penalty=-1,
        messages=[
                {"role": "system", "content": "Esti un sistem de corupere al frazelor in limba romana"},
                {"role": "user", "content": message_content}
            ]
        )
    
    return desentencefy(to_correct, response['choices'][0]['message']['content'].strip())

def desentencefy(original, corrected):
    if not original or not corrected:  # check for empty strings
        return corrected

    original_list = list(original)
    corrected_list = list(corrected)

    # If the corrected sentence starts with an uppercase letter and the original doesn't,
    # make the first letter of corrected lowercase.
    if corrected_list[0].isupper() and original_list[0].islower():
        corrected_list[0] = corrected_list[0].lower()

    # If the original phrase doesn't start with a quote but the corrected one does,
    # remove the starting quote from the corrected.
    if original_list[0] != '"' and corrected_list[0] == '"':
        corrected_list.pop(0)

    # If the original phrase doesn't end with a quote but the corrected one does,
    # remove the ending quote from the corrected.
    if original_list[-1] != '"' and corrected_list[-1] == '"':
        corrected_list.pop(-1)

    return ''.join(corrected_list)

def add_newline_if_missing(s):
    if not s.endswith('\n'):
        s += '\n'
    return s


if __name__ == "__main__":
    in_file = '../corpus/wiki_clean.txt'
    out_file = '../corpus/wiki_clean_dirty_gpt.txt'

    n = 5

    with open(in_file, 'r', encoding='utf-8') as file:
        with open(out_file, 'w', encoding='utf-8') as output_file:
            for _ in range(n):
                line1 = file.readline()
                line1 = add_newline_if_missing(line1)
                
                line2 = generate_text(line1)
                line2 = add_newline_if_missing(line2)

                output_file.write(line1)
                output_file.write(line2)
