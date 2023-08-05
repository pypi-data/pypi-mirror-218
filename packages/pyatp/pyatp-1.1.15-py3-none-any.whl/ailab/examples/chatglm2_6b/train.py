import os
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_dataset.constant import Sources
from ailab.atp_finetuner.constant import Task, Framework
from ailab.atp_finetuner.finetuner import AILabFinetuner
from ailab.utils.other import install_requiremet

def train_progress(percent: float):
    pass

def install_req():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    install_requiremet(dir_path)

def chatglm2_test():
    # todo     # fixed pretrained in train.py
    pretrained_model_name = os.environ.get("PRETRAINED_MODEL_NAME","chatglm2_6b")
    model_name = os.environ.get("MODEL_NAME")
    dataset_path = os.environ.get("DATASET_PATH")
    output_dir = os.environ.get("OUTPUT_DIR", f"/work/model/{model_name}")
    pretrained_model_path = os.environ.get("PRETRAINED_MODEL_PATH", f"/home/.atp/models/{pretrained_model_name}")
    tokenizer_path = os.environ.get("TOKENIZER_PATH")

    if not pretrained_model_name or not model_name or not dataset_path or not pretrained_model_path or not tokenizer_path:
        raise TypeError(
            f'os.environ should have (PRETRAINED_MODEL_NAME,MODEL_NAME,DATASET_PATH,TOKENIZER_PATH)')

    dataset = AILabDataset.load_dataset(dataset_path, src=Sources.huggingface)
    args = {
        "model_args": {
        },
        "train_args": {
            "output_dir": output_dir,
            "save_strategy": "steps",
            "learning_rate": 5e-4,
            "per_device_train_batch_size": 2,
            "gradient_accumulation_steps": 2,
            "num_train_epochs": 10,
            "logging_steps": 10,
            "fp16": True,
            "optim": "adamw_torch",
            "save_steps": 1000,
            "resume_from_checkpoint": True,
        },
    }
    finetuner = AILabFinetuner(Task.question_answering, Framework.Pytorch, dataset,
                               pretrained_model_name, train_progress,
                               pretrained_model_path,
                               tokenizer_path,
                               **args)
    finetuner.finetuner()


if __name__ == '__main__':
    install_req()
    chatglm2_test()
