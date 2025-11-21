import pytest
import requests
import time
import multiprocessing
from app import app


def run_server():
    """启动服务器"""
    app.run(port=5000)


def test_checkout_basic():
    """基本测试"""
    print("🚀 启动测试...")

    # 启动服务器
    server = multiprocessing.Process(target=run_server)
    server.start()
    time.sleep(2)  # 等待服务器启动

    try:
        # 测试1: 正常结算
        print("1. 测试正常结算...")
        data = {"items": [{"price": 20, "quantity": 3}]}
        response = requests.post("http://127.0.0.1:5000/checkout", json=data)
        assert response.status_code == 200
        assert response.json()["total"] == 60
        print("✅ 正常结算测试通过")

        # 测试2: 多个商品
        print("2. 测试多个商品...")
        data = {"items": [
            {"price": 10, "quantity": 2},
            {"price": 5, "quantity": 4}
        ]}
        response = requests.post("http://127.0.0.1:5000/checkout", json=data)
        assert response.status_code == 200
        assert response.json()["total"] == 40  # 10*2 + 5*4 = 40
        print("✅ 多个商品测试通过")

        # 测试3: 空购物车
        print("3. 测试空购物车...")
        data = {"items": []}
        response = requests.post("http://127.0.0.1:5000/checkout", json=data)
        assert response.status_code == 400
        print("✅ 空购物车测试通过")

        # 测试4: 健康检查
        print("4. 测试健康检查...")
        response = requests.get("http://127.0.0.1:5000/health")
        assert response.status_code == 200
        print("✅ 健康检查测试通过")

        print("🎉 所有测试通过！")

    finally:
        # 停止服务器
        server.terminate()
        server.join()


if __name__ == "__main__":
    test_checkout_basic()