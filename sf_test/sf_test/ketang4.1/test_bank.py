import pytest
from unittest.mock import patch, MagicMock
from bank import transfer


def test_transfer_normal():
    """测试跨用户正常转账"""
    # 准备测试数据
    accountA = {"balance": 100, "user": "Alice"}
    accountB = {"balance": 50, "user": "Bob"}

    # 执行转账
    result = transfer(accountA, accountB, 30)

    # 验证结果
    assert result == True
    assert accountA["balance"] == 70
    assert accountB["balance"] == 80


def test_transfer_insufficient_balance():
    """测试余额不足的情况"""
    accountA = {"balance": 20, "user": "Alice"}
    accountB = {"balance": 50, "user": "Bob"}

    # 验证会抛出余额不足异常
    with pytest.raises(ValueError, match="余额不足"):
        transfer(accountA, accountB, 50)


def test_transfer_negative_amount():
    """测试负数金额的情况"""
    accountA = {"balance": 100, "user": "Alice"}
    accountB = {"balance": 50, "user": "Bob"}

    # 验证会抛出无效金额异常
    with pytest.raises(ValueError, match="转账金额必须为正数"):
        transfer(accountA, accountB, -10)


def test_transfer_zero_amount():
    """测试零金额的情况"""
    accountA = {"balance": 100, "user": "Alice"}
    accountB = {"balance": 50, "user": "Bob"}

    # 验证会抛出无效金额异常
    with pytest.raises(ValueError, match="转账金额必须为正数"):
        transfer(accountA, accountB, 0)


def test_transfer_exact_balance():
    """测试刚好用完余额的情况"""
    accountA = {"balance": 50, "user": "Alice"}
    accountB = {"balance": 50, "user": "Bob"}

    result = transfer(accountA, accountB, 50)

    assert result == True
    assert accountA["balance"] == 0
    assert accountB["balance"] == 100


def test_transfer_with_mock():
    """使用unittest.mock测试边界条件"""
    # 创建模拟账户
    mock_accountA = {"balance": 100}
    mock_accountB = {"balance": 50}

    # 使用patch模拟可能的外部依赖
    with patch('builtins.print') as mock_print:
        result = transfer(mock_accountA, mock_accountB, 30)

        # 验证转账成功
        assert result == True
        assert mock_accountA["balance"] == 70
        assert mock_accountB["balance"] == 80


def test_transfer_account_immutability():
    """测试转账不改变账户的其他属性"""
    accountA = {"balance": 100, "user": "Alice", "account_id": "001"}
    accountB = {"balance": 50, "user": "Bob", "account_id": "002"}

    original_userA = accountA["user"]
    original_userB = accountB["user"]
    original_idA = accountA["account_id"]
    original_idB = accountB["account_id"]

    transfer(accountA, accountB, 30)

    # 验证余额变化
    assert accountA["balance"] == 70
    assert accountB["balance"] == 80

    # 验证其他属性不变
    assert accountA["user"] == original_userA
    assert accountB["user"] == original_userB
    assert accountA["account_id"] == original_idA
    assert accountB["account_id"] == original_idB


# 参数化测试，覆盖多种边界情况
@pytest.mark.parametrize("balanceA,balanceB,amount,should_succeed", [
    (100, 50, 30, True),  # 正常情况
    (100, 50, 100, True),  # 刚好转完
    (100, 50, 101, False),  # 余额不足
    (100, 50, -10, False),  # 负数金额
    (100, 50, 0, False),  # 零金额
    (0, 50, 10, False),  # 零余额
])
def test_transfer_parameterized(balanceA, balanceB, amount, should_succeed):
    """参数化测试多种边界情况"""
    accountA = {"balance": balanceA}
    accountB = {"balance": balanceB}

    if should_succeed:
        result = transfer(accountA, accountB, amount)
        assert result == True
        assert accountA["balance"] == balanceA - amount
        assert accountB["balance"] == balanceB + amount
    else:
        with pytest.raises(ValueError):
            transfer(accountA, accountB, amount)