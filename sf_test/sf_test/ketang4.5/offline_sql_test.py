from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)


# 初始化数据库
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # 插入测试用户
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  ('admin', '123456'))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  ('user1', 'password1'))
    except:
        pass

    conn.commit()
    conn.close()


# 有 SQL 注入漏洞的登录函数
def unsafe_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # 危险：直接拼接 SQL 查询（存在 SQL 注入漏洞）
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"执行的 SQL: {query}")  # 打印 SQL 以便调试

    c.execute(query)
    user = c.fetchone()
    conn.close()

    return user is not None


# 安全的登录函数（用于对比）
def safe_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # 安全：使用参数化查询
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
              (username, password))
    user = c.fetchone()
    conn.close()

    return user is not None


@app.route('/')
def home():
    return "SQL 注入测试服务器"


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    # 使用不安全的登录方法
    if unsafe_login(username, password):
        return jsonify({"status": "success", "message": "登录成功"})
    else:
        return jsonify({"status": "error", "message": "用户名或密码错误"}), 400


@app.route('/safe-login', methods=['POST'])
def safe_login_route():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    # 使用安全的登录方法
    if safe_login(username, password):
        return jsonify({"status": "success", "message": "登录成功"})
    else:
        return jsonify({"status": "error", "message": "用户名或密码错误"}), 400


if __name__ == '__main__':
    init_db()
    print("数据库初始化完成")
    print("启动服务器: http://127.0.0.1:5000")

    # 修复：关闭 debug 模式，避免 watchdog 兼容性问题
    app.run(debug=False, port=5000)