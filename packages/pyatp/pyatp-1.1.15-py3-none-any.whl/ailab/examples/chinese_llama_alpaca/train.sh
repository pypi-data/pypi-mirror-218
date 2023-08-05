current_dir=$(dirname "$0")
train_imp_path="$current_dir/train_imp.py"
torchrun --nnodes 1 --nproc_per_node 8 $train_imp_path