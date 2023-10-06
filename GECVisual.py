# Import necessary libraries and modules
import torch
from transformers import AutoTokenizer, RobertaForMaskedLM, RobertaForTokenClassification, MT5ForConditionalGeneration
from Levenshtein import distance as levenshtein_distance  # Import Levenshtein distance function for string similarity calculation
from sklearn.metrics.pairwise import cosine_similarity  # Import function to compute cosine similarity between vectors
import re  # Import regex module for string operations
from flask import Flask, jsonify, request  # Import Flask classes and functions for web app
from flask_cors import CORS  # Import CORS to handle Cross-Origin Resource Sharing

# Initialize Flask application
app = Flask(__name__)

CORS(app)# Enable CORS on the Flask app

# Load tokenizer and add custom tokens
tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-base', model_max_length=128)
custom_tokens = [f"<extra_id_{i}>" for i in range(100)]
tokenizer.add_tokens(custom_tokens)

mt5_model_directory = "models/mt5-base-finetuned-unmask/checkpoint-28000"

# Load pre-trained models for masked language modeling and token classification
model_masked = RobertaForMaskedLM.from_pretrained('xlm-roberta-large')
mt5_model= MT5ForConditionalGeneration.from_pretrained(mt5_model_directory)
mt5_tokenizer = AutoTokenizer.from_pretrained(mt5_model_directory)
add_model_base= RobertaForTokenClassification.from_pretrained("models/add-roberta", local_files_only=True)
mod_model_base= RobertaForTokenClassification.from_pretrained("models/delete-modify-roberta", local_files_only=True)
add_model_gpt= RobertaForTokenClassification.from_pretrained("models/add-roberta-100k", local_files_only=True)
mod_model_gpt= RobertaForTokenClassification.from_pretrained("models/delete-modify-roberta-100k", local_files_only=True)

# Declare a global variable to store data
global all_data

# Function to generate deletion and modification actions on inputs
def generate_del_mod(inputs, model):
    with torch.no_grad():
        if model == "base":
            logits = mod_model_base(**inputs).logits
        if model == "gpt":
            logits = mod_model_gpt(**inputs).logits

    predicted_token_class_ids = logits.argmax(-1)
    return predicted_token_class_ids[0].numpy().tolist()

# Similar function for generating addition actions on inputs
def generate_add(inputs, model):
    with torch.no_grad():
        if model == "base":
            logits = add_model_base(**inputs).logits
        if model == "gpt":
            logits = add_model_gpt(**inputs).logits

    predicted_token_class_ids = logits.argmax(-1)
    return predicted_token_class_ids[0].numpy().tolist()

# Function to generate text using the MT5 model
def generate_mt5(input_text):
  input_ids = mt5_tokenizer(input_text, return_tensors="pt").input_ids.to("cpu")
  output = mt5_model.generate(input_ids, max_length=200)
  return mt5_tokenizer.decode(output[0], skip_special_tokens=True)

# Function to calculate percentage similarity using Levenshtein distance
def procentage_similarity(Q, Mi):
  levDis = levenshtein_distance(Q, Mi)
  bigger = max(len(Q), len(Mi))
  return (bigger - levDis) / bigger


# Additional utility functions for text processing and modification
def combine_add(original, to_replace, nr_of_tokens):
    for i in range(nr_of_tokens):
        result = re.search(custom_tokens[i]+'(.*)'+custom_tokens[i+1], to_replace)
        original = original.replace(custom_tokens[i], result.group(1))
    
    return original


def correct_mod(inputs):
    outputs = model_masked(**inputs)
    predictions = outputs[0]
    sorted_preds, sorted_idx = predictions[0].sort(dim=-1, descending=True)
    predicted_index = [sorted_idx[i, 0].item() for i in range(0,len(sorted_idx))]
    return predicted_index


def score(input_ids):
    """Calculate the perplexity of a batch of tokenized sentences."""
    with torch.no_grad():
        loss = model_masked(input_ids, labels=input_ids).loss
    return torch.exp(loss).tolist()  # Perplexity is the exponential of the loss


# Compute the cosine similarity between two embeddings.
def calculate_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# Convert a token id to its corresponding token.
def decode(id):
    return tokenizer.convert_ids_to_tokens(id)

# Main function to perform correction on the input text.
# Perform correction on the input text based on the specified model and mode.
# Model can be ["base", "gpt"] and mode can be ["base", "mt5"]
# The base models are trained on the 10M dataset, and the gpt models are trained on the 100k custom made dataset
# In "mt5" mode, the system inserts variable-length generated text as deemed necessary by the ADD RoBERTa model.
def correct(text, model, mode):
    inputs = tokenizer(text, return_tensors="pt")
    if len(inputs['input_ids'] > 128):
        pass
    
    all_data["input_ids"] = inputs['input_ids'].tolist()

    decoded = list(map(decode, inputs['input_ids']))

    all_data["input_ids_decoded"] = decoded

    out_mod = generate_del_mod(inputs, model)
    out_add = generate_add(inputs, model)

    all_data["out_mod"] = out_mod.copy()
    all_data["out_add"] = out_add.copy()

    mod_i = 0
    to_mod = inputs
    to_mod = to_mod['input_ids'][0]

    while mod_i != len(out_mod):
        if out_mod[mod_i] == 2:
            to_mod = torch.cat((to_mod[:mod_i], to_mod[mod_i+1:]))
            out_mod.pop(mod_i)

            if mode == 'mt5':
                add = out_add[mod_i]
                out_add.pop(mod_i)
                if add != 0:
                    #print("WE HAVE ONE")
                    #print(text)
                    if mod_i != len(out_add):
                        out_add[mod_i] += add
                    else:
                        out_add[mod_i - 1] += add
            continue
        mod_i += 1

    mod_i = 0

    while mod_i != len(out_mod):

        if out_mod[mod_i] == 1:
            t2 = torch.tensor([250001])
            to_mod = torch.cat((to_mod[:mod_i], t2, to_mod[mod_i+1:]))

        mod_i += 1
    
    to_mod_inter = inputs
    to_mod_inter['input_ids'] = to_mod.unsqueeze(0)
    to_mod_inter['attention_mask'] = torch.ones(to_mod.size()).unsqueeze(0)
    res = correct_mod(to_mod_inter)
    all_data["corrected_no_mt5"] = list(map(decode, res))
    if mode == 'mt5':
        appearences = 0
        for i in range(len(out_add)):
            if out_add[i] == 1:
                extra = 250002 + appearences
                res.insert(i, extra)
                appearences +=1
        to_mt5 = tokenizer.decode(res[1:-1])
        all_data["corrected_no_mt5"] = list(map(decode, res))
        out_mt5 = generate_mt5(to_mt5)
        all_data["out_mt5"] = out_mt5
        to_mt5 = combine_add(to_mt5, out_mt5, appearences)
        to_mt5 = to_mt5.strip()
        final_tokens = tokenizer(to_mt5)
        final_tokens = final_tokens['input_ids']
        all_data["corrected_mt5"] = list(map(decode, final_tokens))
        return to_mt5 + '\n'
    else:
         return tokenizer.decode(res[1:-1]) + '\n'

# Set up a route to receive data through POST requests at the endpoint '/receive-data'.
@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    global all_data
    all_data = {}
    corrected = correct(data["text"], data["model"], data["mode"])
    all_data["corrected"] = corrected
    # Process and use the received data as needed
    return jsonify(all_data)

# Start the Flask application, making it accessible at 'http://0.0.0.0:5000/'.
app.run(host='0.0.0.0', port=5000)