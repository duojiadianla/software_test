from flask import Flask, request, jsonify
from modules import Order

app = Flask(__name__)
order = Order()  # 初始化订单服务

@app.route("/")  # 根路径
def index():
    return "订单系统接口：<br>1. 查库存：/stock/商品名<br>2. 下单：/order?product=商品名&num=数量&amount=金额"
@app.route("/order", methods=["POST"])
def create_order():
    """创建订单接口"""
    data = request.args  # 简化用GET参数（或用json）
    product = data.get("product")
    num = int(data.get("num", 0))
    amount = float(data.get("amount", 0))

    result = order.create(product, num, amount)
    return jsonify(result)


@app.route("/stock/<product>")
def get_stock(product):
    """查库存接口"""
    return jsonify({"product": product, "stock": order.inv.stock.get(product, 0)})


if __name__ == "__main__":
    app.run(debug=False)  # 直接启动服务