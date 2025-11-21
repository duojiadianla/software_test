def transfer(accountA, accountB, amount):
    """
    从账户A向账户B转账

    Args:
        accountA: 转出账户字典，包含'balance'键
        accountB: 转入账户字典，包含'balance'键
        amount: 转账金额

    Returns:
        bool: 转账成功返回True

    Raises:
        ValueError: 当转账金额为负数或余额不足时
    """
    if amount <= 0:
        raise ValueError("转账金额必须为正数")

    if accountA['balance'] < amount:
        raise ValueError("余额不足")

    accountA['balance'] -= amount
    accountB['balance'] += amount
    return True