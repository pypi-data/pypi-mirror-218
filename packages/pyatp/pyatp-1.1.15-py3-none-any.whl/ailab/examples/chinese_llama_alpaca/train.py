import os
from ailab.utils.other import install_requiremet

def install_req():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    install_requiremet(dir_path)

def chinese_alpaca_test():
    import subprocess
    # 启动 shell 脚本
    dir_path = os.path.dirname(os.path.realpath(__file__))
    shell_path = os.path.join(dir_path,"train.sh")
    subprocess.run(["sh", shell_path])

if __name__ == '__main__':
    install_req()
    chinese_alpaca_test()
