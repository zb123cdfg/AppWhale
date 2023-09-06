import sys 
import pyfiglet 
import argparse
import shutil
from pathlib import Path 

sys.path.append("..")
from utils import *


def unzip(apk_path:Path,output_dir:Path):
    extract_apk_contents(apk_path,output_dir)
    if output_dir.joinpath('AndroidManifest.xml').exists():
        return 0
    return 1


def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',help = 'A config file containing APK path',type = str,required=True)
    parser.add_argument('--clean',help = 'Clean all file above',action = 'store_true')
    return parser.parse_args()

if __name__ == '__main__':
    print(pyfiglet.figlet_format('unzip_apk'))

    args = argument()
    apk_dirs = open(args.config,'r').read().splitlines()
    
    for apk in apk_dirs:
        print_focus(f'[unzip] {apk}')
        apk_path = Path(apk)
        output_dir = apk_path.parent.joinpath('out')
        if args.clean:
            shutil.rmtree(output_dir,ignore_errors=True)
        else:
            ret = unzip(apk_path,output_dir)
            if ret == 1:
                print_failed('[unzip] failed')
            else:
                print_success('[unzip] success')
                

