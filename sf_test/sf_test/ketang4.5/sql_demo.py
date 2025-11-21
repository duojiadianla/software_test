# 最简单的 SQL 注入离线演示
print("🔓 SQL 注入攻击演示")
print("=" * 50)

print("📊 模拟数据库内容:")
print("用户表: users")
print("  ID | 用户名 | 密码")
print("  ---|--------|------")
print("  1  | admin  | 123456")
print("  2  | user1  | password1")

print("\n" + "=" * 50)
print("1. 正常登录查询:")
print("-" * 30)

normal_sql = "SELECT * FROM users WHERE username = 'admin' AND password = '123456'"
print(f"SQL: {normal_sql}")
print("✅ 结果: 返回 admin 用户的数据")
print("✅ 登录成功")

print("\n2. SQL 注入攻击:")
print("-" * 30)

injection_sql = "SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = 'anything'"
print(f"SQL: {injection_sql}")
print("💡 攻击原理:")
print("   - ' 闭合了用户名字段")
print("   - OR 1=1 永远为真")
print("   - -- 注释掉了后面的密码检查")
print("❌ 结果: 返回所有用户数据")
print("❌ 攻击者无需密码即可登录！")

print("\n3. 更多攻击示例:")
print("-" * 30)

attacks = [
    ("admin' --", "绕过密码检查，直接登录admin"),
    ("' OR '1'='1", "永远为真条件"),
    ("x' OR id=1 --", "获取ID为1的用户"),
]

for sql, description in attacks:
    print(f"{description}:")
    print(f"  SQL: SELECT ... WHERE username = '{sql}' AND password = 'x'")
    print("  ❌ 攻击成功")

print("\n" + "=" * 50)
print("🛡️ 防护方法:")
print("1. 使用参数化查询:")
safe_code = '''
cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?", 
    (username, password)
)
'''
print(safe_code)
print("2. 输入验证和过滤")
print("3. 最小权限原则")

print("\n" + "=" * 50)
print("🎯 课堂作业完成!")
print("✅ 理解了 SQL 注入原理")
print("✅ 看到了攻击效果")
print("✅ 学习了防护方法")