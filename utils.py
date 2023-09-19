import os
import zipfile
from rich.console import Console
from pathlib import Path
from subprocess import Popen,PIPE,STDOUT,TimeoutExpired

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

def shell_cmd(cmd:str,env:dict = None,timeout:int = None):
    os.environ['PATH'] += ':' + str(Path('~/.local/bin').expanduser())
    local_env = env.copy() if env else os.environ
    cwd = local_env.pop('cwd',None)
    cwd = Path(cwd).expanduser() if cwd else cwd
    exe = local_env.pop('exe','sh')
    if gradle := local_env.pop('gradle',None):
        change_gradle = {
            4:'sdk use gradle 4.10.3',
            5:'sdk use gradle 5.6.4',
            6:'sdk use gradle 6.9.4',
            7:'sdk use gradle 7.6.1'
        }
        cmd = f'{change_gradle[gradle]} && {cmd}'
        exe = 'zsh'
    if java := local_env.pop('java',None):
        change_java = {
            8:'sdk use java 8.0.372-tem',
            11:'sdk use java 11.0.19-tem'
        }
        cmd = f'{change_java[java]} && {cmd}'
        exe = 'zsh'
    
    p1 = Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT,cwd=cwd,env=local_env,executable=f'/bin/{exe}')
    try:
        output = p1.communicate(timeout=timeout)[0].decode('utf-8',errors='replace')
        ret_code = p1.returncode
    except TimeoutExpired:
        print('Execution timeout!')
        p1.kill()
        output = p1.communicate()[0].decode('utf-8',errors='replace')
        output += '\n\nERROR:execution timed out!'
        ret_code = 1
    return output,ret_code



