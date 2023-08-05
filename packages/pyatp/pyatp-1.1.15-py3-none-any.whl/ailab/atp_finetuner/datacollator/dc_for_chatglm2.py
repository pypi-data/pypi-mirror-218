import torch
from typing import Dict, Optional, Sequence, Union
from transformers import DataCollatorWithPadding,BatchEncoding,PreTrainedTokenizer
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner.constant import Task, Model

class DataCollatorForChatGLM(DataCollatorWithPadding):
        r"""
        Data collator for ChatGLM. It is capable of dynamically padding for batched data.
        """
        def __init__(
                self,
                tokenizer: PreTrainedTokenizer,
                ignore_pad_token_for_loss: Optional[bool] = False
        ):
            super().__init__(tokenizer, padding=True)
            IGNORE_INDEX = -100
            self.label_pad_token_id = IGNORE_INDEX if ignore_pad_token_for_loss else tokenizer.pad_token_id
            self.get_attention_masks = self.get_attention_masks_v2
            self.get_position_ids = self.get_position_ids_v2


        def get_attention_masks_v2(self, input_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
            r"""
            Generates attention masks for left-padded sequences.
            """
            batch_size, seq_length = input_ids.size()
            attention_mask = torch.ones((batch_size, seq_length), device=device)

            for i, seq in enumerate(input_ids):
                attention_mask[i, :(seq != self.tokenizer.pad_token_id).nonzero()[0].item()] = 0 # padding

            return attention_mask

        def get_position_ids_v2(self, input_ids: torch.Tensor, device: torch.device) -> torch.Tensor:
            r"""
            Generates position ids for left-padded sequenes.
            """
            batch_size, seq_length = input_ids.size()
            position_ids = torch.zeros((batch_size, seq_length), dtype=torch.long, device=device)

            for i, seq in enumerate(input_ids):
                padding_length = (seq != self.tokenizer.pad_token_id).nonzero()[0].item()
                position_ids[i, padding_length:] = torch.arange(seq_length - padding_length, dtype=torch.long, device=device)

            return position_ids

        def __call__(self, features: Sequence[Dict[str, Union[torch.Tensor, Sequence[int]]]]) -> BatchEncoding:
            r"""
            Pads batched data to the longest sequence in the batch.

            We adopt left-padding in both training and evaluation.
            """
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

            input_ids = torch.nn.utils.rnn.pad_sequence(
                input_ids,
                batch_first=True,
                padding_value=self.tokenizer.pad_token_id
            ).flip(-1)

            batch = {}

            if "labels" in features[0]:
                input_ids, labels = input_ids.split(len(features), dim=0)
                labels = torch.where(labels != self.tokenizer.pad_token_id, labels, self.label_pad_token_id)
                batch["labels"] = labels

            batch["input_ids"] = input_ids
            batch["attention_mask"] = self.get_attention_masks(input_ids, device=input_ids.device)
            batch["position_ids"] = self.get_position_ids(input_ids, device=input_ids.device)

            return BatchEncoding(batch)

@DataCollatorRg.register((Task.question_answering, Model.chatglm2_6b))
class Chatglm2DataCollator(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)
    
    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor) :
        datacollator = DataCollatorForChatGLM(preprocessor.preprocessor_ins)
        return cls(datacollator, preprocessor)