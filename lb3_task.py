from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Пользовательские данные (логины и пароли)
users = {
    "admin": "password123",
    "user": "mypassword"
}

# Верификация пользователя
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Расширенный каталог товаров с 3 параметрами для каждого товара
catalog = {
    1: {"name": "Arabica", "price": 100.25, "category": "Coffee Beans"},
    2: {"name": "Robusta", "price": 80.50, "category": "Coffee Beans"},
    3: {"name": "Espresso Machine", "price": 1500.00, "category": "Equipment"},
    4: {"name": "French Press", "price": 25.00, "category": "Equipment"},
    5: {"name": "Coffee Mug", "price": 5.75, "category": "Accessories"},
    6: {"name": "Milk Frother", "price": 30.00, "category": "Equipment"},
    7: {"name": "Decaf Arabica", "price": 95.00, "category": "Coffee Beans"},
}

# Эндпоинт для работы со всем каталогом
@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def handle_items():
    if request.method == 'GET':
        return jsonify({"items": catalog})
    elif request.method == 'POST':
        data = request.json
        if not data or "name" not in data or "price" not in data or "category" not in data:
            return jsonify({"error": "Invalid data"}), 400
        new_id = max(catalog.keys(), default=0) + 1
        catalog[new_id] = {"name": data["name"], "price": data["price"], "category": data["category"]}
        return jsonify({"message": "Item added", "item": catalog[new_id]}), 201

# Эндпоинт для работы с конкретным товаром
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def handle_item(item_id):
    if item_id not in catalog:
        return jsonify({"error": "Item not found"}), 404

    if request.method == 'GET':
        return jsonify({"item": catalog[item_id]})
    elif request.method == 'PUT':
        data = request.json
        if not data or "name" not in data or "price" not in data or "category" not in data:
            return jsonify({"error": "Invalid data"}), 400
        catalog[item_id] = {"name": data["name"], "price": data["price"], "category": data["category"]}
        return jsonify({"message": "Item updated", "item": catalog[item_id]})
    elif request.method == 'DELETE':
        del catalog[item_id]
        return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(debug=True)
