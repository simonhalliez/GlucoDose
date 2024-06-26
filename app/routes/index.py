import base64

import pandas as pd
import requests
from flask import Blueprint, request, jsonify, current_app
from flask import redirect, url_for, render_template, session

home_blueprint = Blueprint('index', __name__)

client_id = current_app.config['CLIENT_ID']
client_secret = current_app.config['CLIENT_SECRET']


def get_access_token():
    token_url = 'https://oauth.fatsecret.com/connect/token'
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'grant_type=client_credentials&scope=basic'
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']


@home_blueprint.route('/', methods=['GET'])
@home_blueprint.route('/home', methods=['GET'])
def home():
    # Take the template in templates and show it
    return render_template("home.html")


@home_blueprint.route('/get-session-ingredients', methods=['GET'])
def get_session_ingredients():
    ingredients = session.get('ingredients', [])
    return jsonify({"ingredients": ingredients})


@home_blueprint.route('/reset-ingredients', methods=['POST'])
def reset_ingredients():
    session.pop('ingredients', None)
    session.modified = True
    return jsonify({"message": "Ingredients reset"}), 200


@home_blueprint.route('/search-food', methods=['POST'])
def search_food():
    query = request.json.get('query')
    token = get_access_token()
    search_url = 'https://platform.fatsecret.com/rest/server.api'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = f'method=foods.search&search_expression={query}&format=json'
    response = requests.post(search_url, headers=headers, data=data)
    response.raise_for_status()
    return jsonify(response.json())


@home_blueprint.route('/save-ingredient', methods=['POST'])
def save_ingredient():
    ingredient = request.json.get('selectedProduct')
    if 'ingredients' not in session:
        session['ingredients'] = []
    session['ingredients'].append(ingredient)
    session.modified = True
    return jsonify({"message": "Ingredient saved"}), 200


@home_blueprint.route('/delete-ingredient', methods=['POST'])
def delete_ingredient():
    ingredient_id = request.json.get('id')
    if 'ingredients' in session:
        session['ingredients'] = [i for i in session['ingredients'] if i['id'] != ingredient_id]
        session.modified = True
    return jsonify({"message": "Ingredient deleted"}), 200


@home_blueprint.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    # Post when press submit button
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # session is like a python dico specific to the user and accessible every where in the back end
        session["username"] = username
        return redirect("/user_page")
    else:
        # if already have a session -> go to user page
        if "username" in session:
            return redirect("/user_page")
        return render_template("sign_in.html")


@home_blueprint.route("/user_page")
def user_page():
    if "username" in session:
        username = session["username"]
        # Pass the username in argument to recover and display it on the page, we can do it with list for
        # the favorit meal of the user
        return render_template("user_page.html", user=username)
    else:
        # no session -> go to sign in
        return redirect("/sign_in")


@home_blueprint.route("/account_creation", methods=["POST", "GET"])
def account_creation():
    if request.method == "POST":
        print("Account")
        username = request.form["username"]
        password = request.form["password"]
        return redirect("/sign_in")
    return render_template("account_creation.html")


@home_blueprint.route("/foodstuffs_selection")
def foodstuffs_selection():
    data = pd.read_csv('nutrients_csvfile.csv')
    list_food_stucks = []
    for index, row in data.iterrows():
        list_food_stucks.append(
            {'label': row['Food'], 'carbs': row['Carbs'], 'image_link': url_for('static', filename='images/Default_image.png')})
    return render_template("foodstuffs_selection.html", list_food_stucks=list_food_stucks)


@home_blueprint.route("/meal_resume", methods=["POST", "GET"])
def meal_resume():
    if request.method == "POST":

        data = request.get_json()
        print(data)
        if not data or 'glucose_level' not in data or 'glucose_goal' not in data or 'insulin_sensitivity' not in data:
            return jsonify({"error": "Invalid input"}), 400

        session["glucose_level"] = data['glucose_level']
        session["glucose_goal"] = data['glucose_goal']
        session["insulin_sensitivity"] = data['insulin_sensitivity']

        # Réponse en JSON
        response = {
            'message': 'Données reçues avec succès',
            'received_data': data
        }
        return jsonify(response)
    if ("username" in session):
        return render_template("meal_resume.html", haveSession=True)
    return render_template("meal_resume.html", haveSession=False)


@home_blueprint.route("/log_out")
def log_out():
    session.pop("username", None)
    return redirect("/home")
