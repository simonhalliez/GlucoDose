import couchdb
from flask import Blueprint, request, jsonify, current_app
from app.models import Ingredient, InsulinCalculation

insulin_blueprint = Blueprint('insulin', __name__)


@insulin_blueprint.route('/compute', methods=['POST'])
def compute_insulin():
    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({"error": "Invalid input"}), 400

    ingredients_data = data['ingredients']
    ingredients = []
    for item in ingredients_data:
        try:
            name = item['name']
            quantity = item['quantity']
            ingredient = Ingredient(name, quantity)
            ingredients.append(ingredient)
        except KeyError:
            return jsonify({"error": "Invalid ingredient format"}), 400

    insulin_calc = InsulinCalculation(ingredients)
    insulin_dose = insulin_calc.calculate_insulin_dose()

    return jsonify({"total_insulin_dose": insulin_dose}), 200


@insulin_blueprint.route('/combinations', methods=['POST'])
def save_combination():
    data = request.get_json()
    if not data or 'ingredients' not in data or 'insulinLevel' not in data:
        return jsonify({"error": "Invalid input"}), 400

    db = current_app.config['COUCHDB_DB']
    doc = {
        "type": "combination",
        "ingredients": data['ingredients'],
        "insulinLevel": data['insulinLevel']
    }
    db.save(doc)
    return jsonify({"message": "Combination saved successfully"}), 201


@insulin_blueprint.route('/combinations', methods=['GET'])
def get_saved_combinations():
    db = current_app.config['COUCHDB_DB']
    combinations = [doc for doc in db if doc.get('type') == 'combination']
    if not combinations:
        return jsonify({"error": "No combinations found"}), 404
    return jsonify(combinations), 200


@insulin_blueprint.route('/combinations/<id>', methods=['GET'])
def get_combination(id):
    db = current_app.config['COUCHDB_DB']
    try:
        doc = db[id]
        if doc.get('type') != 'combination':
            return jsonify({"error": "Combination not found"}), 404
        return jsonify(doc), 200
    except couchdb.ResourceNotFound:
        return jsonify({"error": "Combination not found"}), 404
