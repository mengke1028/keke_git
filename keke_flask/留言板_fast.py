import sqlite3
import logging
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify,render_template_string
import os
os.system("color")
os.system("")  # 这一句会开启 VT100 模拟

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 session 的密钥
app.config['TRUST_PROXIES'] = True
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 创建日志目录
LOG_FOLDER = 'logs'
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
VALID_ACCESS_CODE = '1'
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'  # 重置颜色
    

def create_connection():
    try:
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        # 检查 messages 表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        table_exists = cursor.fetchone()

        if table_exists:
            # 检查 timestamp 列是否存在
            cursor.execute("PRAGMA table_info(messages)")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            column_names = column_names[:10]
            if 'timestamp' not in column_names:
                # 如果 timestamp 列不存在，则添加该列
                cursor.execute("ALTER TABLE messages ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP")
            if 'image' not in column_names:
                # 如果 image 列不存在，则添加该列
                cursor.execute("ALTER TABLE messages ADD COLUMN image TEXT")
        else:
            # 如果表不存在，则创建表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    image TEXT
                )
            ''')

        conn.commit()
        return conn
    except Exception as e:
        logging.error(f"数据库连接或表创建出错: {e}")
        return None


@app.route('/')
def index():
    # 获取当前日期和时间
    now = datetime.datetime.now()
    # 获取当前是星期几，0 表示周一，4 表示周五
    weekday = now.weekday()
    # 获取当前小时数
    hour = now.hour
    # 判断是否满足条件
    template = '留言板_工作.html'
    if 0 <= weekday <= 4 and 6 <= hour <= 18:
        pass
    else:
        if not session.get('is_authenticated'):
            # 可以返回一个简单的验证页面，或让前端处理未验证状态
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>访问验证</title>
                <style>
                    /* 简单样式优化，避免页面空白等待 */
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f0f2f5;
                    }
                   .loading {
                        color: #666;
                        font-size: 16px;
                    }
                </style>
            </head>
            <body>
                <!-- 加载提示，验证完成前显示 -->
                <div class="loading">验证中，请稍候...</div>
    
                <script>
                    document.addEventListener('DOMContentLoaded', function () {
                        // 显示访问码输入框
                        let userInput = prompt('请输入访问码以继续访问：');
    
                        if (userInput === null) {
                            // 用户取消输入，跳转指定页面
                            window.location.href = 'https://www.biquai.cc/';
                            return;
                        }
    
                        // 去除输入前后空格（避免误输入空格导致验证失败）
                        userInput = userInput.trim();
    
                        if (userInput === '') {
                            // 输入为空，提示后重新弹窗
                            alert('访问码不能为空，请重新输入');
                            window.location.reload(); // 刷新页面重新验证
                            return;
                        }
    
                        // 发送验证请求
                        fetch('/verify-access', {
                            method: 'POST',
                            headers: { 
                                'Content-Type': 'application/json',
                                'X-Requested-With': 'XMLHttpRequest' // 标识为AJAX请求
                            },
                            body: JSON.stringify({ code: userInput })
                        })
                       .then(response => {
                            // 处理HTTP错误状态（如500服务器错误）
                            if (!response.ok) {
                                throw new Error('验证服务异常');
                            }
                            return response.json();
                        })
                       .then(data => {
                            if (data.valid) {
                                // 验证通过，刷新页面加载主内容
                                window.location.reload();
                            } else {
                                // 验证失败，提示后跳转
                                alert('访问码错误，无法访问');
                                window.location.href = 'https://www.biquai.cc/';
                            }
                        })
                       .catch(err => {
                            console.error('验证失败:', err);
                            alert('验证过程出错，请稍后再试');
                            window.location.href = 'https://www.biquai.cc/';
                        });
                    });
                </script>
            </body>
            </html>
            ''')

    # 第二步：已验证，才执行数据库操作并渲染模板

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            WITH ranked_messages AS (
                SELECT *,
                       ROW_NUMBER() OVER (
                           PARTITION BY name, message 
                           ORDER BY timestamp DESC
                       ) as rn
                FROM messages
            )
            SELECT id, name, message, timestamp, image
            FROM ranked_messages
            WHERE rn = 1
            ORDER BY timestamp DESC
            LIMIT 20;
            """
            cursor.execute(query)
            # cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC')
            messages = cursor.fetchall()



            # 记录访问日志
            x_forwarded_for = request.headers.get('X-Forwarded-For')
            if x_forwarded_for:
                user_ip = x_forwarded_for.split(',')[0].strip()
            else:
                user_ip = request.remote_addr
            log_message = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 用户 {user_ip} 访问了首页\n"
            with open(os.path.join(LOG_FOLDER, 'access.log'), 'a') as log_file:
                print(f"{Color.GREEN}{log_message}{Color.END}")

                log_file.write(log_message)
            print(messages)
            return render_template(template, messages=messages)
        except Exception as e:
            logging.error(f"查询留言出错: {e}")
        finally:
            conn.close()
    return "发生错误，请稍后重试"


@app.route('/verify-access', methods=['POST'])
def verify_access():
    """访问码验证接口"""
    data = request.get_json()
    user_input = data.get('code') if data else None
    print("user_input", user_input)
    if user_input == VALID_ACCESS_CODE:
        session['is_authenticated'] = True
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})


@app.route('/add_message', methods=['POST'])
def add_message():
    name = request.form.get('name')
    message = request.form.get('message')
    image = request.files.get('image')

    image_filename = None
    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)
        image_filename = image.filename

    if name and message:
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                current_time = datetime.datetime.now()
                cursor.execute('INSERT INTO messages (name, message, timestamp, image) VALUES (?,?,?,?)',
                               (name, message, current_time, image_filename))
                conn.commit()
                # 发送新留言事件到客户端
                new_message = {
                    'name': name,
                    'message': message,
                    'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'image': image_filename
                }
                print(name, message)
                return redirect(url_for('index'))
            except Exception as e:
                logging.error(f"插入留言出错: {e}")
            finally:
                conn.close()
    logging.error("留言提交失败，姓名或留言为空")
    return "留言提交失败，请检查输入"

@app.route('/suijirenwu')
def suijirenwu():
    """随机任务"""
    return render_template('随机任务.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/set_username', methods=['POST'])
def set_username():
    data = request.get_json()
    username = data.get('username')
    if username:
        session['username'] = username
        return 'OK'
    return 'No username provided', 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)