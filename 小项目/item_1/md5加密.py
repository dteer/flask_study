import hashlib

def md5(arg):
    hash = hashlib.md5('ghjkl;')
    hash.update(bytes(arg,encoding='utf-8'))
    ret = hash.hexdigest()
    return hash.hexdigest()

#解压文件

import shutil
#通过open打开压缩文件，读取内容在进行解压（可二进制，str）
shutil._unpack_zipfile(r'xx.zip')