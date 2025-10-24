from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from datetime import datetime
app = Flask(__name__)

import os
os.system("color")
os.system("")  # 这一句会开启 VT100 模拟

# 设置最大上传文件大小为 2GB (2 * 1024^3 字节)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024

# 设定文件保存的目录，这里假设为当前目录下的uploads文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
VALID_ACCESS_CODE = '1'
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'  # 重置颜色
    
@app.route('/', methods=['GET'])
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0].strip()
    else:
        user_ip = request.remote_addr
    log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 用户 {user_ip} 访问了首页\n"
    print(f"{Color.GREEN}{log_message}{Color.END}")
    return render_template('文件上传.html')


@app.route('/verify-access', methods=['POST'])
def verify_access():
    """访问码验证接口"""
    data = request.get_json()
    user_input = data.get('code') if data else None
    print("user_input",user_input)
    if user_input == VALID_ACCESS_CODE:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "File uploaded successfully", 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/uploads1/<filename>', methods=['GET'])
def uploads1_file(filename):
    # 支持范围请求，实现流式传输
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, conditional=True)

@app.route('/get_audio_files', methods=['GET'])
def get_audio_files():
    audio_files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        # 获取文件的修改时间和文件大小
        modified_time = os.path.getmtime(file_path)
        file_size = os.path.getsize(file_path)
        uploadTime = os.path.getctime(file_path)
        # 将时间戳转换为 datetime 对象
        dt_object = datetime.fromtimestamp(uploadTime)

        # 格式化为常见的日期时间字符串
        uploadTime = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        audio_files.append({
            'name': filename,
            'size': file_size,
            'modified_time': modified_time,
            'uploadTime':uploadTime
        })
    # 按修改时间降序排序
    audio_files.sort(key=lambda x: x['modified_time'], reverse=True)

    return jsonify({'files': audio_files})

if __name__ == '__main__':
    app.run(debug=True, port=5888, host='0.0.0.0')