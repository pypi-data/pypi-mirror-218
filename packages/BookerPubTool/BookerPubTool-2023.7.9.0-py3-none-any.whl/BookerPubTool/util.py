import subprocess as subp
from datetime import datetime
import requests
from pyquery import PyQuery as pq
import tempfile
import uuid
import sys
import shutil
import os
from os import path
import re
import stat
import jieba
import xpinyin

numPinyinMap = {
    '0': 'ling',
    '1': 'yi',
    '2': 'er',
    '3': 'san',
    '4': 'si',
    '5': 'wu',
    '6': 'liu',
    '7': 'qi',
    '8': 'ba',
    '9': 'jiu',
}

def extname(fname):
    m = re.search(r'\.(\w+)$', fname.lower())
    return m.group(1) if m else ''

def gen_proj_name(name):
    # 转小写并移除扩展名
    name = re.sub(r'\.\w+$', '', name.lower())
    # 提取字母数字和中文，分别处理
    seg = re.findall(r'[\u4e00-\u9fff]+|[a-z0-9]+', name)
    nseg = []
    p = xpinyin.Pinyin()
    for s in seg:
        # 字母数字直接添加
        # 中文分词之后转拼音
        if re.search(r'[a-z0-9]', s):
            nseg.append(s)
        else:
            subseg = jieba.cut(s)
            for ss in subseg:
                nseg.append(p.get_pinyin(ss).replace('-', ''))
    res = '-'.join(nseg)
    # 数字开头的加上 x 
    if re.search(r'^\d', res): res = 'x' + res
    # 移除字母数字减号之外的所有字母
    res = re.sub(r'[^a-z0-9\-]', '', res)
    return res

def npm_filter_name(name):
    name = re.sub(r'[^\w\-]', '-', name)
    name = '-'.join(filter(None, name.split('-')))
    
    def rep_func(m):
        s = m.group()
        return ''.join(numPinyinMap.get(ch, '') for ch in s)
    
    name = re.sub(r'\d{2,}', rep_func, name)
    return name

def rmtree(dir):
    files = os.listdir(dir)
    for f in files:
        f = path.join(dir, f)
        if path.isdir(f):
            rmtree(f)
        else:
            os.chmod(f, stat.S_IWUSR)
            os.unlink(f)
    os.rmdir(dir)

def d(name):
    return path.join(path.dirname(__file__), name)

def read_file(name, enco=None):
    mode = 'r' if enco else 'rb'
    with open(name, mode, encoding=enco) as f:
        return f.read()
        
def write_file(name, data, enco=None, append=False):
    mode = 'a' if append else 'w'
    if isinstance(data, bytes):
        mode += 'b'
    with open(name, mode, encoding=enco) as f:
        f.write(data)

def get_desc(md):
    rm = re.search(r'^# (.+?)$', md, re.M)
    return rm.group(1) if rm else ''

def request_retry(method, url, retry=10, check_status=False, **kw):
    kw.setdefault('timeout', 10)
    for i in range(retry):
        try:
            r = requests.request(method, url, **kw)
            if check_status: r.raise_for_status()
            return r
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print(f'{url} retry {i}')
            if i == retry - 1: raise e
