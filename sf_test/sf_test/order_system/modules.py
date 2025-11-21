# 库存模块
class Inventory:
    def __init__(self):
        self.stock = {"apple": 20, "banana": 10}  # 仅保留2个商品

    def check_stock(self, product, num):
        """检查库存是否足够"""
        return self.stock.get(product, 0) >= num

    def reduce_stock(self, product, num):
        """扣减库存"""
        if self.check_stock(product, num):
            self.stock[product] -= num
            return True
        return False


# 支付模块
class Payment:
    def pay(self, amount):
        """模拟支付（仅检查金额>0）"""
        return amount > 0


# 订单模块
class Order:
    def __init__(self):
        self.inv = Inventory()
        self.pay = Payment()
        self.orders = {}  # 存储订单
        self.order_id = 1

    def create(self, product, num, amount):
        """创建订单核心流程"""
        # 1. 查库存
        if not self.inv.check_stock(product, num):
            return {"status": "fail", "msg": "库存不足"}

        # 2. 扣库存
        if not self.inv.reduce_stock(product, num):
            return {"status": "fail", "msg": "库存扣减失败"}

        # 3. 支付
        if not self.pay.pay(amount):
            self.inv.stock[product] += num  # 支付失败回滚库存
            return {"status": "fail", "msg": "支付失败（金额需>0）"}

        # 4. 生成订单
        order_id = f"ORD{self.order_id}"
        self.orders[order_id] = {"product": product, "num": num, "amount": amount}
        self.order_id += 1

        return {"status": "success", "msg": "订单创建成功", "order_id": order_id}