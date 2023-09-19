import os
from pathlib import Path
import threading
import argparse
import pyfiglet
import sys 
import json
import subprocess
sys.path.append('..')
from utils import *





def analysis(apk_path:Path):
    jadx_java = apk_path.parent.joinpath('jadx_java')
    java_file = jadx_java.joinpath('resources/lib/arm64-v8a')
    report_file = apk_path.parent.joinpath('SecScan/test_debug_symbol.json')
    for root,_,files in os.walk(java_file):
        for filename in files:
            file_path = os.path.join(root,filename)
            command = f'nm -a "{file_path}"'
            try:
                output,ret_code = shell_cmd(command)
                print_success("command execute succeed")
                # print(output)
            except subprocess.CalledProcessError as e:
                print_failed("command execute failed")
                # output = ""
            if ret_code == 0:
                with open(report_file,'a+',newline="\n",encoding="utf-8") as json_file:
                    json.dump({"output":output},json_file,ensure_ascii=False,indent=4)


def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='A config file containing APK path', type=str, required=True)
    return parser.parse_args()

if __name__ == '__main__':
    print(pyfiglet.figlet_format('apk_checkDebugSymbol'))
    args = argument()
    apk_dirs = open(args.config, 'r').read().splitlines()
    for apk in apk_dirs:
        print_focus(f'[checkdebugsymbol] {apk}')
        apk_path = Path(apk)

        analysis(apk_path)