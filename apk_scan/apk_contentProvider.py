from pathlib import Path
import xml.etree.ElementTree as ET
import json 
import pyfiglet
import argparse
import sys 


sys.path.append('..')
from utils import *
name_space = "{http://schemas.android.com/apk/res/android}"
def analysis(apk_path:Path):
    exported_provider = {
        "AppInfo":{},
        "ExportedProviders":{}

    }
    app_info_dict = {}
    jadx_java = apk_path.parent.joinpath('jadx_java')
    java_file = jadx_java.joinpath('resources/AndroidManifest.xml')
    output_file = apk_path.parent.joinpath('SecScan/ContentProvider.json')
    tree = ET.parse(java_file)
    root = tree.getroot()
    minsdkVersion = (root.find("uses-sdk").get(name_space + "minSdkVersion"))

    # print(type(minsdkVersion))
    targetsdkVersion = (root.find(".//uses-sdk").get(name_space + "targetSdkVersion"))
    label_value = root.find("application").get(name_space + "label")
    if label_value.startswith("@string/"):
    # 提取字符串资源名称
        resource_name = label_value.split("/")[1]

        # 打开 strings.xml 文件并查找相应的字符串资源
        strings_tree = ET.parse(jadx_java.joinpath('resources/res/values/strings.xml')) # 请替换为您的 strings.xml 文件路径
        strings_root = strings_tree.getroot()

        # 查找具有匹配名称的字符串资源
        for string_element in strings_root.findall(".//string[@name='" + resource_name + "']"):
            AppName = string_element.text
    else:
        # 如果 android:label 属性的值不引用字符串资源，则直接输出它的值
        AppName = label_value
    package_name = root.get("package")
    app_info_dict["AppName"] = AppName
    app_info_dict["packagename"] = package_name
    app_info_dict["minSdkVersion"] = int(minsdkVersion)
    app_info_dict["targetSdkVersion"] = int(targetsdkVersion)
    exported_provider["AppInfo"] = app_info_dict
    if minsdkVersion >= "17" and targetsdkVersion >= "17":
        for elem in root.iter():
        
            if elem.tag == "provider" and elem.get(name_space + "exported") == "true":
                print(elem.get(name_space + "name"))
                elem_dict = {}
                temp_dict = {}
                # elem_content = elem.text
                # print(elem_content)
                elem_dict["readPermission"] = elem.get(name_space + "readPermission")
                elem_dict["writePermission"] = elem.get(name_space + "writePermission")
                elem_dict["permission"] = elem.get(name_space + "permission")
                temp_dict[elem.get(name_space + "name")] = elem_dict
                if exported_provider["ExportedProviders"]:
                    exported_provider["ExportedProviders"].append(temp_dict)
                else:
                    exported_provider["ExportedProviders"] = temp_dict
        with open(output_file,"w") as f:
            json.dump(exported_provider,f,indent=4)


def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='A config file containing APK path', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    print(pyfiglet.figlet_format('apk_contentProvider'))
    # tools_path = Path(__file__).absolute().parents[1].joinpath('tools')

    apk_dirs = open(argument().config, 'r').read().splitlines()

    for apk in apk_dirs:
        print_focus(f'[contentprovider] {apk}')
        apk_path = Path(apk)

        report_path = apk_path.parent.joinpath('SecScan')
        report_path.mkdir(parents=True, exist_ok=True)

        if ret := analysis(apk_path):
            print_failed('[scanner] failed')
        else:
            print_success('[scanner] success')

                    



