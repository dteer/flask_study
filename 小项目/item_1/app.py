import uuid

from flask import Flask,request,render_template
import os
app  = Flask(__name__)
#允许请求的最大字节数 :7M
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 7

from werkzeug.datastructures import FileStorage
FileStorage.save


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    file_obj = request.files.get('code')
    #1、检查上传文件的后缀名
    name_ext = file_obj.filename.rsplit('.',maxsplit=1)
    if len(name_ext) !=2:
        return '请上传zip压缩文件'
    if name_ext[1] !='zip':
        return '请上传zip压缩文件'

    """
    #2、接收用户上传文件
    file_path = os.path.join('files',file_obj.filename)
    #从file_obj.stream 中读取内容，写入文件
    file_obj.save(file_path)

    #3、解压zip文件
    import shutil
    # 通过open打开压缩文件，读取内容在进行解压（可二进制，str）
    shutil._unpack_zipfile(file_path,'xxxx')
    """

    # 2+3，接收用户上传文件，并解压到指定目录
    import shutil
    target_path = os.path.join('files',str(uuid.uuid4()))
    shutil._unpack_zipfile(file_obj.stream,target_path)
    return '上传成功'

if __name__ == '__main__':
    app.run()