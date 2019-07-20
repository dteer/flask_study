import hashlib
import os

#md5加密
def md5(arg):
    hash = hashlib.md5('ghjkl;')
    hash.update(bytes(arg,encoding='utf-8'))
    ret = hash.hexdigest()
    return hash.hexdigest()

#解压文件

def jieya():
    import shutil
    #通过open打开压缩文件，读取内容在进行解压（可二进制，str）
    shutil._unpack_zipfile(r'xx.zip')


#遍历目录并获取py文件中的行数
def Han():
    total_num =0
    for base_path,folder_list,file_list in os.walk('/home/tang/item/'):
        for file_name in file_list:
            file_path = os.path.join(base_path,file_name)
            file_ext = file_path.rsplit('.',maxsplit=1)
            if len(file_ext) !=2:
                continue
            if file_ext[1] != 'py':
                continue

            file_num = 0
            with open(file_path,'rb') as f:
                for line in f:
                    file_num +=1
            total_num +=file_num
    return total_num
