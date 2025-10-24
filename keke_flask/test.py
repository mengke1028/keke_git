from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 首页：返回一个简单的 HTML + JS
HTML = """
<!DOCTYPE html>
<html>
<body>
<script>
let userInput = prompt('请输入内容：');

// 如果用户点了确定，就发送到后端
if (userInput !== null) {
    fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userInput })
    })
    .then(res => res.json())
    .then(data => {
        alert('后端已收到：' + data.received);
    });
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/save', methods=['POST'])
def save_input():
    data = request.get_json()
    user_input = data.get('input', '')
    print('后端收到:', user_input)  # 在终端输出
    return jsonify(received=user_input)

if __name__ == '__main__':
    app.run(debug=True)