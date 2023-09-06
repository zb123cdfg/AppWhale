import os
import zipfile
from rich.console import Console


console = Console()

def print_success(msg:str):
    console.print(f'[+] \{msg}' if msg.startswith('[') else f'[+] {msg}',style = 'bold green')
def print_failed(msg:str):
    console.print(f'[-] \{msg}' if msg.startswith('[') else f'[-] {msg}',style = 'bold red')
def print_focus(msg:str):
    console.print(f'[*] \{msg}' if msg.startswith('[') else f'[*] {msg}',style = 'bold yellow') 


def extract_apk_contents(apk_file,output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with zipfile.ZipFile(apk_file,'r') as apk_zip:
            apk_zip.extractall(output_dir)
        print_success("APK文件内容成功提取到 {}".format(output_dir))
    except Exception as e:
        print_failed("提取APK文件内容时出现错误: {}".format(e))
