import os
from pathlib import Path
import threading
import argparse
import pyfiglet
import sys 
import json

sys.path.append('..')
from utils import *


count_root_detect = 0

def check_for_root_detection(file_path):
    try:
        with open(file_path,"r",encoding='utf-8',errors="ignore") as f:
            file_contents = f.read()
            if any(keyword in file_contents.lower() for keyword in ["superuser","supersu","/xbin/","/sbin/",
                                                                ]):
                return True
    except Exception as e:
            pass
    
    return False



            
def analysis(apk_path:Path):
    jadx_java = apk_path.parent.joinpath('jadx_java')
    java_file = jadx_java.joinpath('sources')
    report_file = apk_path.parent.joinpath('SecScan/test_root_detection.json')
    count_root_detect = 0
    for root,_,files in os.walk(java_file):
        for filename in files:
            file_path = os.path.join(root,filename)
            if file_path.endswith(".java"):
                root_detected = check_for_root_detection(file_path)
                if root_detected:

                    print(f"root detection found in:{file_path}")
                    count_root_detect += 1
    if count_root_detect == 0:
       
            with open(f'{report_file}','w') as f:
                json.dump("No Root detection mechanism found in the APK",f)
        
    else:
       
            with open(f'{report_file}','w') as f:
                json.dump("It seems that root detection mechanism has been implemented",f)

def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='A config file containing APK path', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    print(pyfiglet.figlet_format('apk_checkRootDetection'))
    args = argument()
    apk_dirs = open(args.config, 'r').read().splitlines()
    for apk in apk_dirs:
        print_focus(f'[checkrootdetection] {apk}')
        apk_path = Path(apk)

        analysis(apk_path)






        
