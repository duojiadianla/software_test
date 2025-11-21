from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/checkout", methods=["POST"])
def checkout():
    """简化版结算接口"""
    data = request.get_json()
    items = data.get("items", [])

    # 基本验证
    if not items:
        return jsonify({"error": "购物车为空"}), 400

    # 计算总金额
    total = 0
    for item in items:
        price = item.get("price", 0)
        quantity = item.get("quantity", 0)
        total += price * quantity

    return jsonify({"total": total, "status": "success"}), 200


@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=5000)