from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/mt5-base"

task = "unmask"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def preprocess_function(examples):
    inputs = examples["input"]
    targets = examples["output"]

    input_encodings = tokenizer(inputs, truncation=True, max_length=128)
    with tokenizer.as_target_tokenizer():
        target_encodings = tokenizer(targets, truncation=True, max_length=64)

    # Manually pad the sequences and attention masks to the maximum length
    max_length_input = 128
    max_length_target = 64
    for input_ids, attention_mask in zip(input_encodings['input_ids'], input_encodings['attention_mask']):
        while len(input_ids) < max_length_input:
            input_ids.append(tokenizer.pad_token_id)
            attention_mask.append(0)  # padding tokens should be ignored, so they get a mask value of 0
    for target_ids in target_encodings['input_ids']:
        while len(target_ids) < max_length_target:
            target_ids.append(tokenizer.pad_token_id)

    encodings = {
        'input_ids': input_encodings['input_ids'], 
        'attention_mask': input_encodings['attention_mask'],
        'labels': target_encodings['input_ids'],
    }

    return encodings


train_dataset_dict = load_dataset('json', data_files='./mt5_training.txt')
train_dataset = train_dataset_dict['train']
test_dataset_dict = load_dataset('json', data_files='./mt5_test.txt')
test_dataset = test_dataset_dict['train']

import multiprocessing
num_cores = multiprocessing.cpu_count()

train_dataset_processed = train_dataset.map(preprocess_function, batched=True, num_proc=num_cores, remove_columns=['input', 'output'])
test_dataset_processed = test_dataset.map(preprocess_function, batched=True, num_proc=num_cores, remove_columns=['input', 'output'])

'''training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    load_best_model_at_end=True,
    evaluation_strategy="epoch",
    learning_rate=1e-4,
    save_strategy="epoch",
)'''
batch_size = 48

args = TrainingArguments(
    f"{model_name}-finetuned-{task}",
    evaluation_strategy = "epoch",
    learning_rate=1e-4,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=2,
    weight_decay=0.01,
    save_total_limit = 1,
    save_strategy="steps",
    gradient_accumulation_steps=4,
    #fp16=True,
)


trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset_processed,
    eval_dataset=test_dataset_processed,
    tokenizer=tokenizer,
)

trainer.train()

trainer.save_model("mt5-test")