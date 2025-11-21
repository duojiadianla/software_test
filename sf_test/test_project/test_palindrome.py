"""
回文函数单元测试
"""
import pytest
from palindrome import is_palindrome, is_palindrome_number  # 直接导入


class TestPalindrome:
    """测试字符串回文功能"""

    def test_valid_palindromes(self):
        """测试有效的回文字符串"""
        assert is_palindrome("racecar") == True
        assert is_palindrome("A man a plan a canal Panama") == True
        assert is_palindrome("") == True
        assert is_palindrome("a") == True
        assert is_palindrome("Madam") == True

    def test_invalid_palindromes(self):
        """测试非回文字符串"""
        assert is_palindrome("hello") == False
        assert is_palindrome("python") == False
        assert is_palindrome("not a palindrome") == False

    def test_case_insensitive(self):
        """测试大小写不敏感"""
        assert is_palindrome("RaceCar") == True
        assert is_palindrome("MaDaM") == True

    def test_ignore_spaces(self):
        """测试忽略空格"""
        assert is_palindrome("a man a plan a canal panama") == True
        assert is_palindrome("was it a car or a cat i saw") == True

    def test_invalid_input_type(self):
        """测试无效输入类型"""
        with pytest.raises(TypeError):
            is_palindrome(123)
        with pytest.raises(TypeError):
            is_palindrome([1, 2, 3])
        with pytest.raises(TypeError):
            is_palindrome(None)


class TestPalindromeNumber:
    """测试数字回文功能"""

    def test_valid_palindrome_numbers(self):
        """测试有效的回文数"""
        assert is_palindrome_number(121) == True
        assert is_palindrome_number(1221) == True
        assert is_palindrome_number(0) == True
        assert is_palindrome_number(5) == True

    def test_invalid_palindrome_numbers(self):
        """测试非回文数"""
        assert is_palindrome_number(123) == False
        assert is_palindrome_number(1234) == False
        assert is_palindrome_number(10) == False

    def test_negative_numbers(self):
        """测试负数"""
        assert is_palindrome_number(-121) == False
        assert is_palindrome_number(-5) == False

    def test_invalid_input_type_number(self):
        """测试无效输入类型"""
        with pytest.raises(TypeError):
            is_palindrome_number("121")
        with pytest.raises(TypeError):
            is_palindrome_number(12.1)