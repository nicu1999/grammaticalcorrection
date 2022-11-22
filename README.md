# Romanian Gramatical Error Correction
## What is Gramatical Error Correction
The task of identifying and correcting a grammatical problem in a statement that is grammatically wrong is known as grammar error correction, or GEC. All types of grammatical errors, including as misspellings, improper use of articles, prepositions, pronouns, nouns, etc., as well as weak sentence structure, can be included in this list. GEC is simply an NLP job that trains computers to fix grammar in the same way that humans do. Grammar checkers are used in a variety of applications: email, programs, text editors, messages, and others, to check the grammar of the input text.
## Used resources
The project was done with the help of: jupyter notebooks, the transformers library, the datasets library, the https://github.com/teodor-cotet/RoGEC dataset, cross language RoBERTa, numpy and torch.
## How it works
There are 3 parts to this project: token tagging (TokenTagging.ipynb), training the model (TagTrain.ipynb) and wraping it all up (GEC_final.ipynb).
### Token tagging 
In this phase the goal is to make mask of how to get from the initial, wrong phrase, to the final correct one. An example:
> Wrong: Acoperișul din șindrilă nu se mai păstrează, fiind înlocuită cu țiglă în 1936, fapt ce a necesitat sprijinirea acoperișului cu structuri inprovizate.

> Correct: Acoperișul din șindrilă nu se mai păstrează, fiind înlocuită cu țiglă în 1936, fapt ce a necesitat sprijinirea acoperișului cu structuri improvizate.

The result of running the above example trough TokenTagging.ipynb is the following json object: 

>{"input_ids": [0, 62, 587, 17152, 9511, 202, 321, 828, 29887, 25846, 315, 40, 409, 30650, 9297, 5783, 4, 13374, 200002, 2622, 314, 6, 1878, 177, 25846, 346, 44500, 4, 27444, 405, 10, 34255, 18, 97823, 20884, 84603, 9511, 941, 314, 206199, 23, 70628, 77632, 5, 2], "attention_mask": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "labels": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0], "add_mask": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

The "input_ids" represents the ids of the tokens (we are using the roBERTa tokenizer), the "labels" represent the tokens that are marked for change (1) or deletion (2). I have used a modified dynamic programming levenshtain algorithm to find de differences betweem the wrong version of the sentance and the correct one.

### Training the Model

The base model used is the xlm-roberta-base (cross language model and fine tune it for token classification. The token we are classifying are, of course, weather to delete a token or to modify it.

### Wraping it all up

One of the task roBERTa is trained on is token masking, meaning that a token is removed, and the model is tasked with quessing which token was deleted. The model is using this to its advantage. The basic ideea is that a finetuned roBERTa on toke classification highlights the tokens that should be deleted (trivial) and those that should be replaced (using an out of the box roBERTa model used for token masking).
