import os
from pathlib import Path
import threading
import argparse
import pyfiglet
import sys 
import json
import subprocess
import re 

sys.path.append('..')
from utils import *





def analysis(apk_path:Path):
    jadx_java = apk_path.parent.joinpath('jadx_java')
    java_file = jadx_java.joinpath('resources/lib/arm64-v8a')
    output_file = apk_path.parent.joinpath('SecScan/test_security_property.txt')
    for root,_,files in os.walk(java_file):
        for filename in files:
            file_path = os.path.join(root,filename)
            command = f'checksec --file="{file_path}"'
            # command = f'checksec --file="{file_path}"'
            # try:
            #     output,ret_code = shell_cmd(command)
            #     # print_success("command execute succeed")
            #     print(output)
            # except subprocess.CalledProcessError as e:
            #     print_failed("command execute failed")
            #     # output = ""
            # if ret_code == 0:
            #     with open(report_file,'a+',newline="\n") as json_file:
            #         json.dump(json.loads(output),json_file,indent=4)
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    for line in process.stdout:
                        # 使用正则表达式删除控制字符序列
                        clean_line = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)
                        # print(clean_line, end='')  # 输出到终端，删除控制字符序列
                        file.write(clean_line)     # 将处理后的输出写入文件
                    process.wait()
                print(f"checksec output saved to {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error executing checksec command: {e}")

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='A config file containing APK path', type=str, required=True)
    return parser.parse_args()

if __name__ == '__main__':
    print(pyfiglet.figlet_format('apk_checkSecurityProperty'))
    args = argument()
    apk_dirs = open(args.config, 'r').read().splitlines()
    for apk in apk_dirs:
        print_focus(f'[checksecurityproperty] {apk}')
        apk_path = Path(apk)

        analysis(apk_path)