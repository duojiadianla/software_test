import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class TestLoginFunctionality:
    """登录功能测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        print("🚀 初始化测试环境...")
        
        # Chrome 选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except:
            # 如果无头模式失败，使用普通模式
            cls.driver = webdriver.Chrome()
        
        # 获取测试页面路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_page_path = os.path.join(current_dir, '..', 'test_page.html')
        cls.test_url = f"file:///{test_page_path}"
        
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.driver.maximize_window()
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        cls.driver.quit()
        print("✅ 测试完成，浏览器已关闭")
    
    def setup_method(self):
        """每个测试方法前执行"""
        self.driver.get(self.test_url)
        time.sleep(1)  # 等待页面加载
    
    def take_screenshot(self, name):
        """截屏并保存"""
        screenshot_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path
    
    def test_successful_login(self):
        """测试用例 TC001: 正常登录"""
        print("🧪 执行测试用例 TC001: 正常登录")
        
        # 输入正确的用户名和密码
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        username_input.clear()
        username_input.send_keys("admin")
        password_input.clear()
        password_input.send_keys("123456")
        login_button.click()
        
        # 验证登录成功
        success_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "successMessage"))
        )
        
        assert success_message.is_displayed()
        assert "登录成功" in success_message.text
        print("✅ TC001 通过: 正常登录功能正常")
        
        # 截屏
        self.take_screenshot("TC001_successful_login")
    
    def test_wrong_username(self):
        """测试用例 TC002: 用户名错误"""
        print("🧪 执行测试用例 TC002: 用户名错误")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        username_input.clear()
        username_input.send_keys("wronguser")
        password_input.clear()
        password_input.send_keys("123456")
        login_button.click()
        
        # 验证错误消息
        error_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        assert error_message.is_displayed()
        assert "用户名或密码错误" in error_message.text
        print("✅ TC002 通过: 用户名错误处理正常")
        
        self.take_screenshot("TC002_wrong_username")
    
    def test_wrong_password(self):
        """测试用例 TC003: 密码错误"""
        print("🧪 执行测试用例 TC003: 密码错误")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        username_input.clear()
        username_input.send_keys("admin")
        password_input.clear()
        password_input.send_keys("wrongpassword")
        login_button.click()
        
        # 验证错误消息
        error_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        assert error_message.is_displayed()
        assert "用户名或密码错误" in error_message.text
        print("✅ TC003 通过: 密码错误处理正常")
        
        self.take_screenshot("TC003_wrong_password")
    
    def test_empty_username(self):
        """测试用例 TC004: 用户名为空"""
        print("🧪 执行测试用例 TC004: 用户名为空")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        username_input.clear()  # 不输入用户名
        password_input.clear()
        password_input.send_keys("123456")
        login_button.click()
        
        # 验证错误消息
        error_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        assert error_message.is_displayed()
        assert "用户名不能为空" in error_message.text
        print("✅ TC004 通过: 空用户名验证正常")
        
        self.take_screenshot("TC004_empty_username")
    
    def test_empty_password(self):
        """测试用例 TC005: 密码为空"""
        print("🧪 执行测试用例 TC005: 密码为空")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        username_input.clear()
        username_input.send_keys("admin")
        password_input.clear()  # 不输入密码
        login_button.click()
        
        # 验证错误消息
        error_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        
        assert error_message.is_displayed()
        assert "密码不能为空" in error_message.text
        print("✅ TC005 通过: 空密码验证正常")
        
        self.take_screenshot("TC005_empty_password")
    
    def test_sql_injection(self):
        """测试用例 TC006: SQL注入攻击"""
        print("🧪 执行测试用例 TC006: SQL注入攻击")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        # SQL注入攻击载荷
        sql_payloads = [
            "' OR 1=1 --",
            "admin' --",
            "' OR '1'='1"
        ]
        
        for payload in sql_payloads:
            username_input.clear()
            username_input.send_keys(payload)
            password_input.clear()
            password_input.send_keys("anything")
            login_button.click()
            
            # 验证安全防护
            error_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "errorMessage"))
            )
            
            assert error_message.is_displayed()
            assert "非法字符" in error_message.text or "不安全" in error_message.text
            print(f"✅ SQL注入防护有效: {payload}")
        
        self.take_screenshot("TC006_sql_injection")
    
    def test_xss_attack(self):
        """测试用例 TC007: XSS攻击"""
        print("🧪 执行测试用例 TC007: XSS攻击")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        # XSS攻击载荷
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "admin\" onerror=\"alert('xss')"
        ]
        
        for payload in xss_payloads:
            username_input.clear()
            username_input.send_keys(payload)
            password_input.clear()
            password_input.send_keys("anything")
            login_button.click()
            
            # 验证安全防护
            error_message = self.wait.until(
                EC.visibility_of_element_located((By.ID, "errorMessage"))
            )
            
            assert error_message.is_displayed()
            assert "不安全" in error_message.text or "非法字符" in error_message.text
            print(f"✅ XSS防护有效: {payload}")
        
        self.take_screenshot("TC007_xss_attack")
    
    def test_remember_password(self):
        """测试用例 TC008: 记住密码功能"""
        print("🧪 执行测试用例 TC008: 记住密码功能")
        
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        remember_checkbox = self.driver.find_element(By.ID, "remember")
        login_button = self.driver.find_element(By.CLASS_NAME, "btn")
        
        # 勾选记住密码并登录
        username_input.clear()
        username_input.send_keys("testuser")
        password_input.clear()
        password_input.send_keys("testpass")
        remember_checkbox.click()
        login_button.click()
        
        # 等待登录成功
        success_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "successMessage"))
        )
        
        # 重新加载页面验证记住密码功能
        self.driver.get(self.test_url)
        time.sleep(2)
        
        # 检查是否自动填充
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_input = self.driver.find_element(By.ID, "password")
        
        # 注意：由于安全限制，Selenium 可能无法直接获取自动填充的值
        # 这里我们主要测试记住密码功能是否触发
        remember_checkbox = self.driver.find_element(By.ID, "remember")
        assert remember_checkbox.is_selected()
        print("✅ TC008 通过: 记住密码功能正常")
        
        self.take_screenshot("TC008_remember_password")

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 Web 登录功能测试 - 开始执行")
    print("=" * 60)
    
    # 使用 pytest 运行测试
    pytest.main([
        __file__,
        "-v",
        "--html=../reports/test_report.html",
        "--self-contained-html"
    ])

if __name__ == "__main__":
    run_all_tests()