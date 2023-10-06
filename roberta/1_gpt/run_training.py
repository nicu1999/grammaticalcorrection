import transformers
from transformers import  AutoTokenizer
from transformers import DataCollatorForTokenClassification
from transformers import DataCollatorWithPadding
import torch
from torch import nn
from transformers import Trainer
from datasets import load_dataset, load_metric
import numpy as np

class DataCollatorForTokenClassificationWithPadding(DataCollatorWithPadding):
    def __call__(self, features):
        label_name = "labels" if "labels" in features[0].keys() else "label_ids"
        labels = [feature[label_name] for feature in features]
        for feature in features:
            feature.pop(label_name, None)
        
        batch = super().__call__(features)

        batch["labels"] = torch.tensor(self.pad_sequence(labels, padding_value=-100), dtype=torch.long)
        return batch

    @staticmethod
    def pad_sequence(sequence, padding_value):
        max_length = max([len(seq) for seq in sequence])
        return [seq + [padding_value] * (max_length - len(seq)) for seq in sequence]

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("labels")
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get("logits")
        loss_fct = nn.CrossEntropyLoss(weight=torch.tensor([1, 7, 7.9], device='cuda'))
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    # Remove ignored index (special tokens)
    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

model_checkpoint = "xlm-roberta-base"

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

toke_tagging_dataset = load_dataset('load_dataset.py')

label_list = toke_tagging_dataset['train'].features['labels'].feature.names

model = transformers.AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=3)

model_name = model_checkpoint.split("/")[-1]
task = 'error_detection'
batch_size = 64

args = transformers.TrainingArguments(
    f"{model_name}-finetuned-{task}",
    evaluation_strategy = "epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=20,
    weight_decay=0.01,
    save_strategy="epoch",
)

data_collator = DataCollatorForTokenClassificationWithPadding(tokenizer)

metric = load_metric("seqeval")

#weights = [1, 7, 7.9]

trainer = Trainer(
    model,
    args,
    train_dataset=toke_tagging_dataset["train"],
    eval_dataset=toke_tagging_dataset["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()

trainer.save_model("delete-modify-roberta")