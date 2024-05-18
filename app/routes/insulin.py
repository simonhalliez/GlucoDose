import couchdb
from flask import Blueprint, request, jsonify, current_app, session
from app.models import Ingredient, InsulinCalculation

insulin_blueprint = Blueprint('insulin', __name__)


def calculate_insulin_dose(blood_glucose_level, target_glucose_level, sensitivity_factor, carbs_intake,
                           insulin_to_carb_ratio):
    """
    Calculate the total insulin dosage based on blood glucose level, target glucose level, sensitivity factor, carbohydrate intake, and insulin-to-carb ratio.

    Parameters:
    blood_glucose_level (float): The current blood glucose level of the patient (mg/dl or mmol/l).
    target_glucose_level (float): The desired blood glucose level (given by doctor, mg/dl or mmol/l).
    sensitivity_factor (float): The expected decrease in blood glucose level per unit of insulin (given by doctor, mg/dl per unit or mmol/l per unit).
    carbs_intake (float): The amount of carbohydrate intake in grams.
    insulin_to_carb_ratio (float): The amount of insulin needed per gram of carbohydrate (e.g., ratio 1:15).

    Returns:
    float: The total insulin dosage.
    """

    # Calculate correction dose
    correction_dose = (blood_glucose_level - target_glucose_level) / sensitivity_factor

    # Calculate meal dose (insulin needed for carbohydrate intake)
    meal_dose = carbs_intake * insulin_to_carb_ratio

    # Total insulin dose
    total_insulin_dose = correction_dose + meal_dose

    return total_insulin_dose


@insulin_blueprint.route('/compute', methods=['POST'])
def compute_insulin():
    ingredientsSession = session.get('ingredients', [])

    if not ingredientsSession:
        return jsonify({"error": "Invalid input"}), 400

    ingredients_data = ingredientsSession

    data = request.get_json()
    if not data or 'glucose_level' not in data or 'glucose_goal' not in data or 'insulin_sensitivity' not in data:
        return jsonify({"error": "Invalid input"}), 400

    glucose_level = data['glucose_level']
    glucose_goal = data['glucose_goal']
    insulin_sensitivity = data['insulin_sensitivity']

    total_carbs = sum(item['carbs'] for item in ingredients_data)

    insulin_dose = calculate_insulin_dose(
        blood_glucose_level=glucose_level,
        target_glucose_level=glucose_goal,
        sensitivity_factor=insulin_sensitivity,
        carbs_intake=total_carbs,
        insulin_to_carb_ratio=1 / insulin_sensitivity
    )

    response = {
        'Insulin': round(insulin_dose, 2),
        'meal': ingredients_data
    }

    return jsonify(response), 200


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
