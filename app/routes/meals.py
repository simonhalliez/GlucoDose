from flask import Blueprint, request, jsonify, current_app
import couchdb

meals_blueprint = Blueprint('meals', __name__)


@meals_blueprint.route('/combinations', methods=['POST'])
def create_meal_combination():
    data = request.get_json()
    if not data or 'name' not in data or 'ingredients' not in data:
        return jsonify({"error": "Invalid input"}), 400

    db = current_app.config['COUCHDB_DB']
    meal_combination = {
        "type": "meal_combination",
        "name": data['name'],
        "ingredients": data['ingredients']
    }
    db.save(meal_combination)
    return jsonify({"message": "Meal combination created successfully"}), 201


@meals_blueprint.route('/combinations', methods=['GET'])
def get_meal_combinations():
    db = current_app.config['COUCHDB_DB']
    meal_combinations = []

    for doc_id in db:
        doc = db[doc_id]
        if doc.get('type') == 'meal_combination':
            meal_combinations.append(doc)

    if not meal_combinations:
        return jsonify({"error": "No meal combinations found"}), 404
    return jsonify(meal_combinations), 200


@meals_blueprint.route('/combinations/<id>', methods=['GET'])
def get_meal_combination(id):
    db = current_app.config['COUCHDB_DB']
    try:
        doc = db[id]
        if doc.get('type') != 'meal_combination':
            return jsonify({"error": "Meal combination not found"}), 404
        return jsonify(doc), 200
    except couchdb.ResourceNotFound:
        return jsonify({"error": "Meal combination not found"}), 404


@meals_blueprint.route('/combinations/<id>', methods=['PUT'])
def update_meal_combination(id):
    data = request.get_json()
    if not data or 'name' not in data or 'ingredients' not in data:
        return jsonify({"error": "Invalid input"}), 400

    db = current_app.config['COUCHDB_DB']
    try:
        doc = db[id]
        if doc.get('type') != 'meal_combination':
            return jsonify({"error": "Meal combination not found"}), 404

        doc['name'] = data['name']
        doc['ingredients'] = data['ingredients']
        db.save(doc)
        return jsonify({"message": "Meal combination updated successfully"}), 200
    except couchdb.ResourceNotFound:
        return jsonify({"error": "Meal combination not found"}), 404


@meals_blueprint.route('/combinations/<id>', methods=['DELETE'])
def delete_meal_combination(id):
    db = current_app.config['COUCHDB_DB']
    try:
        doc = db[id]
        if doc.get('type') != 'meal_combination':
            return jsonify({"error": "Meal combination not found"}), 404

        db.delete(doc)
        return jsonify({"message": "Meal combination deleted successfully"}), 204
    except couchdb.ResourceNotFound:
        return jsonify({"error": "Meal combination not found"}), 404
