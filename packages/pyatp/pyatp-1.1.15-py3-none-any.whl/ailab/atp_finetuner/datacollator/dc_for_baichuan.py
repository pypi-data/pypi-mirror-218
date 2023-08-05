import torch
from typing import Dict, Optional, Sequence, Union
from transformers import DataCollatorWithPadding, BatchEncoding
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner.constant import Task, Model

@DataCollatorRg.register((Task.question_answering, Model.baichuan_7b))
class BaichuanDataCollator(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        IGNORE_INDEX = -100
        self.label_pad_token_id = IGNORE_INDEX
        self.padding = True
        super().__init__(self, preprocessor)

    def get_attention_masks(self, input_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
        r"""
        Generates attention masks for left-padded sequences.
        """
        tokenizer = self._preprocessor.preprocessor_ins
        batch_size, seq_length = input_ids.size()
        attention_mask = torch.ones((batch_size, seq_length), device=device)
        for i, seq in enumerate(input_ids):
            attention_mask[i, :(seq != tokenizer.pad_token_id).nonzero()[0].item()] = 0 # padding
        attention_mask = attention_mask.bool()
        return attention_mask

    def __call__(self, features: Sequence[Dict[str, Union[torch.Tensor, Sequence[int]]]]) -> BatchEncoding:
        r"""
        Pads batched data to the longest sequence in the batch.

        We adopt left-padding in both training and evaluation.
        """
        tokenizer = self._preprocessor.preprocessor_ins
        if isinstance(features[0]["input_ids"], torch.Tensor):
            input_ids = [feature["input_ids"].clone().detach().flip(0) for feature in features]
        else:
            input_ids = [torch.tensor(feature["input_ids"]).flip(0) for feature in features]

        if "labels" in features[0]:
            if isinstance(features[0]["labels"], torch.Tensor):
                labels = [feature["labels"].clone().detach().flip(0) for feature in features]
            else:
                labels = [torch.tensor(feature["labels"]).flip(0) for feature in features]
            input_ids = input_ids + labels # pad them to the same length

        input_ids = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=tokenizer.pad_token_id).flip(-1)

        batch = {}

        if "labels" in features[0]:
            input_ids, labels = input_ids.split(len(features), dim=0)
            labels = torch.where(labels != tokenizer.pad_token_id, labels, self.label_pad_token_id)
            batch["labels"] = labels

        batch["input_ids"] = input_ids
        batch["attention_mask"] = self.get_attention_masks(input_ids, device=input_ids.device)

        return BatchEncoding(batch)
    
    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor) :
        return cls(None, preprocessor)