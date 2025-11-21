from locust import HttpUser, task, between, TaskSet
import random
import json
import time


class OrderBehavior(TaskSet):
    """订单相关行为任务集"""

    def on_start(self):
        """任务集启动时执行"""
        self.user_id = random.randint(1000, 9999)
        self.order_ids = []  # 存储创建的订单ID

    @task(3)
    def create_complex_order(self):
        """创建复杂订单"""
        # 多种产品组合
        product_combinations = [
            [{"product_id": 1, "quantity": 1}],  # 只买笔记本
            [{"product_id": 2, "quantity": 1}],  # 只买手机
            [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 1}],  # 买两样
            [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 2}]  # 买更多
        ]

        items = random.choice(product_combinations)
        order_data = {
            "user_id": self.user_id,
            "items": items
        }

        with self.client.post(
                "/orders",
                json=order_data,
                catch_response=True,
                name="创建复杂订单"
        ) as response:
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    order_id = result["order"]["id"]
                    self.order_ids.append(order_id)

                    # 记录成功的订单
                    self.user.environment.events.request_success.fire(
                        request_type="POST",
                        name="创建复杂订单",
                        response_time=response.elapsed.total_seconds() * 1000,
                        response_length=len(response.text),
                    )

                    # 根据订单金额决定是否支付（金额大的更可能支付）
                    total_amount = result["order"]["total_amount"]
                    payment_probability = min(0.8, total_amount / 10000)  # 金额越大支付概率越高

                    if random.random() < payment_probability:
                        self.pay_order(order_id)
                else:
                    response.failure(f"创建订单业务失败: {result}")
            else:
                response.failure(f"创建订单HTTP失败: {response.status_code}")

    @task(1)
    def view_orders(self):
        """查看已有订单"""
        if self.order_ids:
            order_id = random.choice(self.order_ids)
            with self.client.get(
                    f"/orders/{order_id}",
                    catch_response=True,
                    name="查看订单"
            ) as response:
                if response.status_code != 200:
                    response.failure(f"查看订单失败: {response.status_code}")

    def pay_order(self, order_id):
        """支付订单"""
        with self.client.post(
                f"/orders/{order_id}/pay",
                catch_response=True,
                name="支付订单"
        ) as response:
            if response.status_code == 200:
                result = response.json()
                if not result.get("success"):
                    # 支付失败是正常情况
                    pass


class BrowseBehavior(TaskSet):
    """浏览行为任务集"""

    @task(5)
    def browse_products(self):
        """浏览产品"""
        with self.client.get("/products", name="浏览产品") as response:
            pass

    @task(1)
    def get_specific_product(self):
        """查看特定产品"""
        product_id = random.randint(1, 2)  # 我们只有2个产品
        with self.client.get(f"/products/{product_id}", name="查看特定产品") as response:
            pass


class AdvancedOrderUser(HttpUser):
    """
    高级订单用户 - 结合浏览和下单行为
    """
    wait_time = between(1, 5)

    tasks = [OrderBehavior, BrowseBehavior]

    def on_start(self):
        """用户启动"""
        print(f"高级用户启动")


class SpikeUser(HttpUser):
    """
    峰值测试用户 - 短时间内大量请求
    """
    wait_time = between(0.05, 0.2)  # 非常短的等待时间

    @task(10)
    def spike_order(self):
        """峰值订单"""
        order_data = {
            "user_id": random.randint(100000, 999999),
            "items": [{"product_id": 1, "quantity": 1}]
        }

        self.client.post("/orders", json=order_data, name="峰值订单")