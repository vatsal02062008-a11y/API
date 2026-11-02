from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample menu data. This is stored in memory for demonstration purposes.
MENU = {
    "Water bottle": 20,
    "Pizza": 199,
    "Salad": 120,
    "Sandwich": 80,
    "Waffle": 150,
    "Orange juice": 90,
    "Iced tea": 60,
    "Coffee": 40,
}

_next_order_id = 101


@app.get("/menu")
def get_menu():
    """Return the canteen menu as JSON."""
    return jsonify(MENU), 200


@app.post("/order")
def place_order():
    """Accept an order in JSON and return its confirmation."""
    global _next_order_id

    order = request.get_json(silent=True)
    if not isinstance(order, dict):
        return jsonify({"error": "Send order details as a JSON object."}), 400

    item = order.get("item")
    quantity = order.get("quantity")

    if item not in MENU:
        return jsonify({"error": "Please select an item from the menu."}), 400

    # bool is a subclass of int in Python, so explicitly reject booleans.
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "Quantity must be a positive whole number."}), 400

    total = MENU[item] * quantity
    result = {
        "order_id": _next_order_id,
        "item": item,
        "quantity": quantity,
        "unit_price": MENU[item],
        "total": total,
        "status": "Order Placed",
    }
    _next_order_id += 1

    return jsonify(result), 201


if __name__ == "__main__":
    # Local development server; do not use Flask's debug server in production.
    app.run(host="127.0.0.1", port=5000, debug=True)
