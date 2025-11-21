import pytest
import requests
from modules import Inventory, Payment, Order

# ------------------- 单元测试 -------------------
def test_inventory():
    inv = Inventory()
    assert inv.check_stock("apple", 5) is True  # 库存足够
    assert inv.check_stock("apple", 30) is False  # 库存不足
    inv.reduce_stock("apple", 5)
    assert inv.stock["apple"] == 15  # 扣减成功

def test_payment():
    pay = Payment()
    assert pay.pay(10) is True  # 支付成功
    assert pay.pay(0) is False  # 支付失败

def test_order_success():
    order = Order()
    res = order.create("apple", 2, 20)
    assert res["status"] == "success"  # 订单成功

def test_order_stock_fail():
    order = Order()
    res = order.create("apple", 100, 50)
    assert res["msg"] == "库存不足"  # 库存不足失败

# ------------------- 集成测试（调用API） -------------------
def test_api_order_success():
    # 启动app.py后运行（需保持服务开启）
    res = requests.post("http://127.0.0.1:5000/order",
                        params={"product": "banana", "num": 2, "amount": 10})
    assert res.json()["status"] == "success"

def test_api_order_pay_fail():
    res = requests.post("http://127.0.0.1:5000/order",
                        params={"product": "apple", "num": 1, "amount": 0})
    assert res.json()["msg"] == "支付失败（金额需>0）"