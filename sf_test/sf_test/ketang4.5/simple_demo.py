import sqlite3
import os


def demonstrate_sql_injection():
    """演示 SQL 注入原理"""
    print("🧪 SQL 注入攻击演示")
    print("=" * 50)

    # 创建测试数据库
    conn = sqlite3.connect(':memory:')  # 使用内存数据库，不会创建文件
    c = conn.cursor()

    # 创建用户表
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    ''')

    # 插入测试数据
    c.execute("INSERT INTO users (username, password) VALUES ('admin', '123456')")
    c.execute("INSERT INTO users (username, password) VALUES ('user1', 'password1')")
    conn.commit()

    print("📊 数据库内容:")
    c.execute("SELECT * FROM users")
    for row in c.fetchall():
        print(f"   ID: {row[0]}, 用户名: {row[1]}, 密码: {row[2]}")

    print("\n" + "=" * 50)
    print("1. 正常登录场景:")
    print("-" * 30)

    # 正常登录
    username = "admin"
    password = "123456"
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"🔍 SQL 查询: {query}")

    c.execute(query)
    result = c.fetchone()
    if result:
        print("✅ 登录成功: 用户名和密码正确")
    else:
        print("❌ 登录失败")

    print("\n2. SQL 注入攻击场景:")
    print("-" * 30)

    # SQL 注入攻击
    malicious_username = "' OR 1=1 --"
    any_password = "anything"
    malicious_query = f"SELECT * FROM users WHERE username = '{malicious_username}' AND password = '{any_password}'"
    print(f"🔍 SQL 查询: {malicious_query}")
    print("💡 解释: -- 是 SQL 注释，使得后面的密码检查被忽略")
    print("💡 OR 1=1 永远为真，所以会返回所有用户")

    c.execute(malicious_query)
    results = c.fetchall()
    if results:
        print(f"❌ 漏洞存在！攻击成功返回了 {len(results)} 条记录:")
        for row in results:
            print(f"   ID: {row[0]}, 用户名: {row[1]}, 密码: {row[2]}")
    else:
        print("✅ 攻击被阻止")

    print("\n3. 更多攻击示例:")
    print("-" * 30)

    attacks = [
        ("admin' --", "攻击1: 注释掉密码检查"),
        ("' OR '1'='1", "攻击2: 永远为真条件"),
        ("x' OR id=1 --", "攻击3: 获取特定用户"),
    ]

    for attack_username, description in attacks:
        attack_query = f"SELECT * FROM users WHERE username = '{attack_username}' AND password = 'anything'"
        print(f"\n{description}")
        print(f"🔍 SQL: {attack_query}")

        c.execute(attack_query)
        if c.fetchone():
            print("❌ 攻击成功")
        else:
            print("✅ 攻击失败")

    print("\n" + "=" * 50)
    print("🛡️ 防护方法:")
    print("1. 使用参数化查询:")
    print("   cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))")
    print("2. 对用户输入进行验证")
    print("3. 使用 Web 应用防火墙")

    conn.close()


if __name__ == "__main__":
    demonstrate_sql_injection()