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
