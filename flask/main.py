import base64
import io
import os

import flask
from flask import Flask, request, url_for, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
from mydocx.excel2docx2 import gen

# templates为运行方法同级的模板文件名称
app = Flask(__name__, template_folder='templates')

# 文件上传路径
UPLOAD_FILE_PATH = os.path.join(app.root_path, 'upload_file')

# 允许上传的文件格式
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ppt', 'pptx', 'word', 'wordx'}


# 上传文件名称前都会拼接的前缀
# app.config['UPLOAD_FOLDER'] = 'upload-'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FILE_PATH + '/'


# controller
@app.route("/first")
def first():
    text = "Welcome Flask World ! "
    return text + flask.__version__


@app.route('/sec', methods=['POST', 'GET'])
def second(value):
    print('second' + value)
    return value + 'second'


@app.route('/third/<path:value>')
def third(value):
    print(value)
    return value


@app.route('/')
def index():
    # path = r'login.html'
    path = r'convert.html'
    return render_template(path)


@app.route('/welcome/<name>')
def welcome(name):
    return f'welcome {name}'


# form 表单需要添加 enctype="multipart/form-data"
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            # post请求获取值的方式
            user = request.form['email']
            # 获取文件类型
            file = request.files['file']
            file_name = secure_filename(file.filename)
            if file_name == '':
                raise Exception('please select a file first！')
            file.save(f'{UPLOAD_FILE_PATH}/{file_name}')
            return redirect(url_for('welcome', name=user))
            # return user
        if request.method == 'GET':
            # get请求获取值的方式
            user = request.args.get('username')
            # 获取文件类型
            file = request.files.get('file')
            # return redirect(url_for('welcome', name=user))
            return user
    except Exception as e:
        return str(
            e) + '\n\n\nthere are something wrong happened !! if you cannot solve it \nplease concat the developer soon !!'
    return 'default'


@app.route('/download')
def download():
    path = f'{UPLOAD_FILE_PATH}'
    file_name = 'arthas.log'
    return send_from_directory(path, file_name, as_attachment=False)


def get_word_cloud(text):
    # font = "./SimHei.ttf"
    # pil_img = WordCloud(width=500, height=500, font_path=font).generate(text=text).to_image()

    pil_img = WordCloud(width=800, height=300, background_color="white").generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64


# 生成词云图片接口，以base64格式返回
@app.route('/word/cloud/generate', methods=["GET"])
def cloud():
    text = request.json.get("word")
    res = get_word_cloud(text)
    return res


with app.test_request_context():
    print(url_for('first'))
    print(url_for('second', value='  nihaoa'))


@app.route('/dw/<path:value>')
def download_file(value):
    path = os.path.join(app.root_path, 'download')
    file_name = value
    print('执行了一次')
    return send_from_directory(path, file_name, as_attachment=False)


@app.route('/test/dw')
def test_multi_dw_file():
    print(url_for('download_file', value='arthas.log'))
    print(url_for('download_file', value='main.txt'))
    return 'success'


@app.route('/convert', methods=['POST'])
def convert_file():
    user = request.form['email']
    # 获取文件类型
    file = request.files['file']
    file_name = secure_filename(file.filename)
    if file_name == '':
        raise Exception('please select a file first！')
    file.save(f'{UPLOAD_FILE_PATH}/{file_name}')
    file_list = gen(f'{UPLOAD_FILE_PATH}/{file_name}')
    for i in range(len(file_list)):
        url_for('download_file', value=file_list[i])
    # f = file.read()
    # print(f)
    # with open(f'{UPLOAD_FILE_PATH}/{file_name}', 'r+', encoding='utf-8') as fi:
    #     text = fi.read()
    #     lines = fi.readlines()
    #     line = fi.readline()
    # print(text)
    # print(lines)
    # print(line)
    return 'success'


# 启动类
if __name__ == '__main__':
    app.run(debug=True)
