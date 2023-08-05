import transformers
from transformers import AutoTokenizer
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor

@PreProcessorRg.register((Task.question_answering, Model.baichuan_7b))
class BaichuanPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        tokenizer  = AutoTokenizer.from_pretrained(pc_name_dir,use_fast=False,padding_side="left",trust_remote_code=True)
        tokenizer.pad_token_id = 0 if tokenizer.pad_token_id is None else tokenizer.pad_token_id # set as the <unk> token
        tokenizer.pad_token_id = 0 if tokenizer.pad_token_id == 64000 else tokenizer.pad_token_id # for baichuan model (older version)
        return cls(dataset, tokenizer)

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        dataset = self._dataset.to_hf_dataset()
        dummy_data = [None] * len(dataset)
        for column_name, target_name in [
            ("instruction", "prompt"),
            ("input", "query"),
            ("output", "response"),
            ("history", "history")
        ]: # every dataset will have 4 columns same as each other
            if column_name in dataset.column_names:
                dataset = dataset.rename_column(column_name, target_name)
            else:
                dataset = dataset.add_column(target_name, dummy_data)

        from ailab.utils.template import Template
        column_names = list(dataset.column_names)
        prefix = ""
        prompt_template = Template("default")

        def get_dialog(examples):
            for i in range(len(examples["prompt"])):
                if examples["prompt"][i] and examples["response"][i]:
                    query, answer = examples["prompt"][i], examples["response"][i]
                    query = query + "\n" + examples["query"][i] if examples["query"][i] else query
                    dialog = prompt_template.get_dialog(query, answer, examples["history"][i], prefix)
                    yield dialog
        
        IGNORE_INDEX = -100
        max_source_length = 512
        max_target_length = 512
        def preprocess_supervised_dataset(examples):
            # build inputs with format `X [BOS] Y [EOS]` and labels with format `[IGNORE] ... [IGNORE] Y [EOS]`
            # for input with history, we build multiple input-label pairs just like:
            # https://github.com/lm-sys/FastChat/blob/f17c092f64840fa6354ed52789dccb2daa793d0b/fastchat/train/train.py#L112
            model_inputs = {"input_ids": [], "labels": []}
            for dialog in get_dialog(examples):
                input_ids, labels = [], []

                for i in range(len(dialog) // 2):
                    source_ids = tokenizer.encode(text=dialog[2*i], add_special_tokens=False)
                    target_ids = tokenizer.encode(text=dialog[2*i+1], add_special_tokens=False)
                    input_ids += source_ids + [tokenizer.bos_token_id] + target_ids + [tokenizer.eos_token_id]
                    labels += [IGNORE_INDEX] * (len(source_ids) + 1) + target_ids + [tokenizer.eos_token_id]

                model_inputs["input_ids"].append(input_ids[:max_source_length + max_target_length])
                model_inputs["labels"].append(labels[:max_source_length + max_target_length])
            return model_inputs
    
        tokenized_dataset = dataset.map(preprocess_supervised_dataset,
                                        batched=True,
                                        remove_columns=column_names,)
        return AILabDataset(tokenized_dataset)