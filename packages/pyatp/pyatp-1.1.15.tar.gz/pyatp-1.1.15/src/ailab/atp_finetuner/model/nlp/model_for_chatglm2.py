from types import MethodType
import torch
from transformers import AutoModel,AutoConfig
from peft import TaskType,LoraConfig,get_peft_model
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.question_answering, Model.chatglm2_6b))
class Chatglm2Model(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        model = self.model_ins

        model.lm_head = model.transformer.output_layer
        output_embedding_base_layer = model.transformer
        output_embedding_layer_name = "output_layer"

        layer_norm_names = ["layernorm"] # for chatglm setting
        for name, param in model.named_parameters():
            if param.ndim == 1 and any(layer_norm_name in name for layer_norm_name in layer_norm_names):
                param.data = param.data.to(torch.float32)

        model.enable_input_require_grads()
        model.gradient_checkpointing_enable()
        model.config.use_cache = False # turn off when gradient checkpointing is enabled

        if hasattr(output_embedding_base_layer, output_embedding_layer_name):
            output_embedding_layer = getattr(output_embedding_base_layer, output_embedding_layer_name)
            input_dtype = output_embedding_layer.weight.dtype

            class CastOutputToFloat(torch.nn.Sequential):

                def forward(self, x: torch.Tensor) -> torch.Tensor:
                    return super().forward(x.to(input_dtype)).to(torch.float32)

            setattr(output_embedding_base_layer, output_embedding_layer_name, CastOutputToFloat(output_embedding_layer))
        
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM, # we should regard ChatGLM as a causal LM
            inference_mode=False,
            r=8,
            lora_alpha=32.0,
            lora_dropout=0.1,
            target_modules=['query_key_value'])
        model = get_peft_model(model, lora_config)
        self._model = model
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        config = AutoConfig.from_pretrained(model_name_or_dir, trust_remote_code=True)
        model = AutoModel.from_pretrained(
            model_name_or_dir,
            config=config,
            trust_remote_code=True
        )
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
