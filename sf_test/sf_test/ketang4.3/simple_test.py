from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


# 测试 Chrome 浏览器
def test_chrome():
    print("🧪 测试 Chrome 浏览器")
    try:
        # 启动 Chrome
        driver = webdriver.Chrome()

        # 打开登录页面
        file_path = os.path.abspath("simple_login.html")
        driver.get(f"file:///{file_path}")

        # 检查页面标题
        assert "登录页面" in driver.title
        print("✅ 页面标题正确")

        # 检查页面内容
        assert "用户登录" in driver.page_source
        print("✅ 页面包含登录表单")

        # 测试登录功能
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.TAG_NAME, "button")

        # 输入正确的用户名密码
        username.send_keys("admin")
        password.send_keys("123456")
        login_btn.click()

        time.sleep(1)  # 等待页面响应

        # 检查登录结果
        message = driver.find_element(By.ID, "message")
        assert "登录成功" in message.text
        print("✅ 登录成功测试通过")

        # 测试错误密码
        username.clear()
        password.clear()
        username.send_keys("admin")
        password.send_keys("wrong")
        login_btn.click()

        time.sleep(1)

        message = driver.find_element(By.ID, "message")
        assert "错误" in message.text
        print("✅ 登录失败测试通过")

        driver.quit()
        print("🎉 Chrome 测试完成")

    except Exception as e:
        print(f"❌ Chrome 测试失败: {e}")


# 测试 Firefox 浏览器
def test_firefox():
    print("\n🧪 测试 Firefox 浏览器")
    try:
        # 启动 Firefox
        driver = webdriver.Firefox()

        # 打开登录页面
        file_path = os.path.abspath("simple_login.html")
        driver.get(f"file:///{file_path}")

        # 基本检查
        assert "登录页面" in driver.title
        assert "用户登录" in driver.page_source
        print("✅ 页面加载正常")

        # 截屏保存
        driver.save_screenshot("firefox_test.png")
        print("✅ 截屏已保存")

        driver.quit()
        print("🎉 Firefox 测试完成")

    except Exception as e:
        print(f"❌ Firefox 测试失败: {e}")


if __name__ == "__main__":
    print("🚀 开始浏览器兼容性测试")
    print("=" * 40)

    test_chrome()
    test_firefox()

    print("=" * 40)
    print("📊 所有测试完成！")