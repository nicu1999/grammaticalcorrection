import csv
import json
import os
import datasets

_CITATION = """\
@InProceedings{huggingface:dataset,
title = {XML-RoBERTa Wrong Token Tagging},
author={Rosca Nicolae
},
year={2022}
}
"""
_DESCRIPTION = """\
This dataset is used for token tagging for GEC.
"""

_HOMEPAGE = ""

_LICENSE = ""

_URLS = {
    "token_tagging": ['/content/drive/MyDrive/Colab Notebooks/corpus/big_dataset.txt', '/content/drive/MyDrive/Colab Notebooks/corpus/gold_corpus_test.txt']
}


class loadDataset(datasets.GeneratorBasedBuilder):
    """This dataset is used for token tagging for GEC."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="token_tagging", version=VERSION, description="Token Tagging"),
    ]

    DEFAULT_CONFIG_NAME = "token_tagging"

    def _info(self):
        if self.config.name == "token_tagging":
            features = datasets.Features({"input_ids": datasets.features.Sequence(datasets.Value('int32')), 
                                          "attention_mask": datasets.features.Sequence(datasets.Value('int8')), 
                                          'labels': datasets.features.Sequence(feature=datasets.features.ClassLabel(num_classes=3, names=['ok', 'dif', 'del'], id=None), length=-1, id=None),
                                        })
                                    
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,)

    def _split_generators(self, dl_manager):
        urls = _URLS[self.config.name]
        print(urls)
        data_dir = dl_manager.download_and_extract(urls)
        print(data_dir)
        
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir[0],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir[1],
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                del data['add_mask']
                #data['attention_mask'] = data.pop('attention_mask ')
                #data['input_ids'] = data.pop('input_ids ')
                if self.config.name == "token_tagging":
                    yield key, data