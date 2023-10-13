from pathlib import Path
import xml.etree.ElementTree as ET
import json 
import pyfiglet
import argparse
import sys 


sys.path.append('..')
from utils import *
name_space = "{http://schemas.android.com/apk/res/android}"
normalArray = []
dangerousArray = []
coreArray = []
specialArray = []

def apkPermissionsList(root):
    permissionList = []
    ps = ""
    if root.findall("uses-permission") != None:
        for ps in  root.findall("uses-permission"):
            # print(ps)
            permissionList.append(ps.get(name_space + "name"))
    if root.findall("permission") != None:
        for ps in root.findall("permission"):
            permissionList.append(ps.get(name_space + "name"))
    return permissionList


def apkPermissionLevel(permissionList):
    normal = {
        '访问额外位置 (ACCESS_LOCATION_EXTRA_COMMANDS)': '允许应用软件访问额外的位置提供指令',
        '获取网络连接(ACCESS_NETWORK_STATE)': '允许获取网络连接信息',
        '设置通知(ACCESS_NOTIFICATION_POLICY)': '允许设置通知策略',
        '蓝牙(BLUETOOTH)': '允许应用软件连接配对过的蓝牙设备',
        '管理蓝牙(BLUETOOTH_ADMIN)': '允许应用软件管理蓝牙，搜索和配对新的蓝牙设备',
        '发送持久广播(BROADCAST_STICKY)': '允许应用发送持久广播',
        '更改网络连接状态(CHANGE_NETWORK_STATE)': '允许应用更改网络连接状态，自动切换网络',
        '改变WIFI多播模式 (CHANGE_WIFI_MULTICAST_STATE)': '允许应用进入WIFI多播模式，允许应用使多播地址接收发送到无线 网络上所有设备(而不仅是用户手机)数据包。',
        '更改WIFI连接状态(CHANGE_WIFI_STATE)': '允许应用改变WIFI连接状态',
        '禁用锁屏(DISABLE_KEYGUARD)': '允许应用禁用系统锁屏。允许应用停用键锁以及任何关联的密码安 全措施。例如让手机在接听来电时停用键锁，在通话结束后重新启用键锁。',
        '展开或折叠状态栏(EXPAND_STATUS_BAR)': '允许应用展开和折叠状态栏',
        '前台服务(FOREGROUND_SERVICE)': '允许应用使用前台服务',
        '获取包大小(GET_PACKAGE_SIZE)': '允许应用获取安装包占空间大小',
        '安装桌面快捷方式(INSTALL_SHORTCUT)': '允许应用在桌面安装快捷方式',
        '使用互联网(INTERNET)': '允许应用打开网络接口',
        '后台杀进程(KILL_BACKGROUND_PROCESSES)': '允许应用调用特定方法结束其他应用的后台进程',
        '管理自身通话(MANAGE_OWN_CALLS)': '允许拥有通话功能的应用通过自身连接管理服务接口处理自身的 通话行为',
        '修改音频设置(MODIFY_AUDIO_SETTINGS)': '允许该应用修改移动智能终端音频设置',
        '使用NFC(NFC)': '允许应用使用NFC进行I/O操作，与其他NFC标签、卡和读卡器通信',
        '读取帐户同步设置(READ_SYNC_SETTINGS)': '允许该应用读取某个帐户的同步设置。例如，此权限可确定“联系 人”是否与允许该应用读取某个帐户的同步设置',
        '读取帐户同步统计信息(READ_SYNC_STATS)': '允许该应用读取某个帐户的同步统计信息，包括活动历史记录和数据量',
        '接收启动完成广播(RECEIVE_BOOT_COMPLETED)': '允许应用接收系统启动完成广播',
        '重新排序正在运行的应用(REORDER_TASKS)': '允许应用对正在运行的应用重新排序',
        '请求后台运行(REQUEST_COMPANION_RUN_IN_BACKGROUND)': '允许应用在后台运行',
        '请求后台使用数据(REQUEST_COMPANION_USE_DATA_IN_BACKGROUND )': '允许应用在后台使用数据',
        '请求卸载应用(REQUEST_DELETE_PACKAGES)': '允许应用卸载其他应用',
        '忽略电池优化策略(REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)': '允许应用忽略系统电池优化策略',
        '设置闹钟(SET_ALARM)': '允许应用设置闹钟',
        '设置时区(SET_TIME_ZONE)': '允许应用设置系统时区',
        '设置壁纸(SET_WALLPAPER)': '允许应用设置系统壁纸',
        '设置壁纸提示(SET_WALLPAPER_HINTS)': '允许应用设置有关系统壁纸大小的提示',
        '使用红外线发射器(TRANSMIT_IR)': '允许应用使手机的红外线发射器',
        '删除桌面快捷方式(UNINSTALL_SHORTCUT)': '允许应用删除桌面快捷方式',
        '使用指纹(USE_FINGERPRINT)': '允许应用使手机指纹设备',
        '振动(VIBRATE)': '允许应用使手机振动',
        '唤醒锁(WAKE_LOCK)': '允许应用持有系统唤醒锁，防止进程进入睡眠状态或息屏',
        '修改帐户同步设置(WRITE_SYNC_SETTINGS)': '允许该应用修改某个帐户的同步设置，包括启用和停用同步',
        '读取应用列表(QUERY_ALL_PACKAGES)': '允许应用读取手机上的应用列表，仅适用于target sdk大于等于30以上的Android设备和应用软件'
    }
    dangerous = {
        '读取日历(READ_CALENDAR)': '读取日历内容',
        '写入或删除日历(WRITE_CALENDAR)': '修改日历内容',
        '读取手机识别码(READ_PHONE_STATE)': '允许应用软件读取电话状态',
        '读取联系人(READ_CONTACTS)': '允许应用软件读取联系人通讯录信息',
        '写入或删除联系人(WRITE_CONTACTS)': '允许应用软件写入联系人，但不可读取',
        '访问手机账户列表(GET_ACCOUNTS)': '允许应用软件访问当前手机的账户列表信息',
        '读取传感器(BODY_SENSORS)': '允许应用软件访问用户用来衡量身体内发生的情况的传感器的数据，例如心率',
        '发送短信(SEND_SMS)': '允许应用软件发送短信',
        '接收短信(RECEIVE_SMS)': '允许应用软件接收短信 ',
        '读取短信(READ_SMS)': '允许应用软件读取短信内容 ',
        '接收WAP PUSH(RECEIVE_WAP_PUSH)': '允许应用软件接收WAP PUSH信息 ',
        '接收彩信(RECEIVE_MMS)': '允许应用软件接收彩信 ',
        '读取外部存储空间(READ_EXTERNAL_STORAGE)': '允许应用软件读取扩展存 ',
        '写入外部存储空间(WRITE_EXTERNAL_STORAGE)': '允许应用软件写入外部存储，如SD卡上写文件 ',
        '获取无线状态(ACCESS_WIFI_STATE)': '允许获取无线网络相关信息',
        '读取电话号码(READ_PHONE_NUMBERS)': '允许该应用访问设备上的电话号码',
        '读取小区广播消息(READ_CELL_BROADCASTS)': '允许应用读取您的设备收到的小区广播消息。小区广播消息是在某些地区发送的、用于发布紧急情况警告的提醒信息。恶意应用可能会在您收到小区紧急广播时干扰您设备的性能或操作',
        '从您的媒体收藏中读取位置信息(ACCESS_MEDIA_LOCATION)': '允许该应用从您的媒体收藏中读取位置信息',
        '接听来电(ANSWER_PHONE_CALLS)': '允许该应用接听来电',
        '继续进行来自其他应用的通话(ACCEPT_HANDOVER)': '允许该应用继续进行在其他应用中发起的通话',
        '身体活动(ACTIVITY_RECOGNITION)': '获取您的身体活动数据'
    }
    core = {
        '使用摄像头(CAMERA)': '允许应用软件调用设备的摄像头进行拍摄、录像',
        '访问精确位置(ACCESS_FINE_LOCATION)': '允许应用软件通过GPS获取精确的位置信息 ',
        '访问大致位置(ACCESS_COARSE_LOCATION)': '允许应用软件通过WiFi或移动基站获取粗略的位置信息',
        '在后台使用位置信息(ACCESS_BACKGROUND_LOCATION)': '即使未在前台使用此应用，此应用也可以随时访问位置信息',
        '录音或通话录音(RECORD_AUDIO)': '允许应用获取麦克风输入数据信息 ',
        '使用SIP(USE_SIP)': '允许应用软件使用SIP视频服务 ',
        '拨打电话(CALL_PHONE)': '允许应用软件拨打电话,从非系统拨号器里初始化一个电话拨号',
        '读取通话记录(READ_CALL_LOG)': '允许应用软件读取通话记录',
        '写入通话记录(WRITE_CALL_LOG)': '允许应用软件写入通话记录',
        '使用语音邮件(ADD_VOICEMAIL)': '允许应用软件使用语音邮件',
        '修改外拨电话(PROCESS_OUTGOING_CALLS)': '允许应用软件监视、修改外拨电话'
    }
    sepical = {
        '设备管理器(BIND_DEVICE_ADMIN)': '激活使用设备管理器',
        '辅助模式(BIND_ACCESSIBILITY_SERVICE)': '使用无障碍功能',
        '读写系统设置(WRITE_SETTINGS)': '允许应用读取或写入系统设置',
        '读取应用通知(BIND_NOTIFICATION_LISTENER_SERVICE)': '允许应用读取应用的通知内容',
        '悬浮窗(SYSTEM_ALERT_WINDOW)': '允许应用显示在其他应用之上，或后台弹出界面 ',
        '读取应用使用情况(PACKAGE_USAGE_STATS)': '允许应用读取本机的应用使用情况 ',
        '请求安装应用(REQUEST_INSTALL_PACKAGES)': '允许应用安装其他应用 ',
        '访问所有文件(MANAGE_EXTERNAL_STORAGE)': '允许应用访问分区存储模式下SD卡上的所有文件',
        '应用软件列表(GET_INSTALLED_APPS)': '允许应用读取手机上的应用软件列表'
    }
    
    newPermissionList = permissionList.copy()
    for p in permissionList:
        for key in normal.keys():
            # print(normal.keys())
            # key:访问额外位置 (ACCESS_LOCATION_EXTRA_COMMANDS)
            #     获取网络连接(ACCESS_NETWORK_STATE)
            names = key.split('(')
            # names:['访问额外位置 ', 'ACCESS_LOCATION_EXTRA_COMMANDS)']
            #       ['获取网络连接', 'ACCESS_NETWORK_STATE)']
            if names[-1].strip().replace(')', '') in p.split('.')[-1]:
                normalArray.append((p))
                # print(normalArray)
                newPermissionList.remove(p)
                break
        for key in dangerous.keys():
            names = key.split('(')
            if names[-1].strip().replace(')','') in p.split('.')[-1]:
                dangerousArray.append((p))
                break
        for key in core.keys():
            names = key.split('(')
            if names[-1].strip().replace(')', '') in p.split('.')[-1]:
                coreArray.append((p))
                newPermissionList.remove(p)
                break
        for key in sepical.keys():
            names = key.split('(')
            if names[-1].strip().replace(')', '') in p.split('.')[-1]:
                specialArray.append((p))
                newPermissionList.remove(p)
                break
    return normalArray, dangerousArray, coreArray, specialArray, newPermissionList
     

    
def analysis(apk_path:Path):
    Permissions_description = {
        "AppInfo":{},
        "normal_permissions":[],
        "dangerous_permissions":[],
        "core_permissions":[],
        "special_permissions":[],
        "other_permissions":[]

    }
    app_info_dict = {}
    jadx_java = apk_path.parent.joinpath('jadx_java')
    java_file = jadx_java.joinpath('resources/AndroidManifest.xml')
    output_file = apk_path.parent.joinpath('SecScan/permissions.json')
    tree = ET.parse(java_file)
    root = tree.getroot()
    minsdkVersion = (root.find("uses-sdk").get(name_space + "minSdkVersion"))
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
    Permissions_description["AppInfo"] = app_info_dict

    normalArray,dangerousArray,coreArray,specialArray,newPermissionList = apkPermissionLevel(apkPermissionsList(root))

    Permissions_description['normal_permissions'] = normalArray
    Permissions_description['dangerous_permissions'] = dangerousArray
    Permissions_description['core_permissions'] = coreArray
    Permissions_description['special_permissions'] = specialArray
    Permissions_description['other_permissions'] = newPermissionList
   
    with open(output_file,"w",encoding='utf-8') as f:
        json.dump(Permissions_description,f,ensure_ascii=False,indent=4)   



def argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='A config file containing APK path', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    print(pyfiglet.figlet_format('apk_contentProvider'))
    # tools_path = Path(__file__).absolute().parents[1].joinpath('tools')

    apk_dirs = open(argument().config, 'r').read().splitlines()

    for apk in apk_dirs:
        print_focus(f'[permissions] {apk}')
        apk_path = Path(apk)

        report_path = apk_path.parent.joinpath('SecScan')
        report_path.mkdir(parents=True, exist_ok=True)

        if ret := analysis(apk_path):
            print_failed('[scanner] failed')
        else:
            print_success('[scanner] success')

                    



