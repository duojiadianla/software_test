"""
回文判断模块
"""

def is_palindrome(s):
    """
    判断字符串是否为回文

    Args:
        s (str): 要检查的字符串

    Returns:
        bool: 如果是回文返回True，否则返回False

    Raises:
        TypeError: 如果输入不是字符串
    """
    if not isinstance(s, str):
        raise TypeError("输入必须为字符串")

    # 处理空字符串和单字符情况
    if len(s) <= 1:
        return True

    # 忽略大小写和空格
    cleaned = ''.join(s.lower().split())

    # 检查是否为回文
    return cleaned == cleaned[::-1]


def is_palindrome_number(n):
    """
    判断数字是否为回文数

    Args:
        n (int): 要检查的数字

    Returns:
        bool: 如果是回文数返回True，否则返回False
    """
    if not isinstance(n, int):
        raise TypeError("输入必须为整数")

    return str(n) == str(n)[::-1]