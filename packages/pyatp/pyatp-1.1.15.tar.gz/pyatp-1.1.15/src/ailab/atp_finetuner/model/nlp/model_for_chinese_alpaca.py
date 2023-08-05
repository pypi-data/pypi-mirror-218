from typing import List
import torch
from transformers import LlamaForCausalLM,AutoConfig
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.question_answering, Model.chinese_alpaca))
class ChineseAlpacaModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir

        torch_dtype=torch.float16
        config = AutoConfig.from_pretrained(model_name_or_dir)
        model = LlamaForCausalLM.from_pretrained(
            model_name_or_dir,
            from_tf=bool(".ckpt" in model_name_or_dir),
            config=config,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True
        )
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
