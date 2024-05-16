from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import pandas as pd
app = Flask(__name__)
app.secret_key = "Secret_key"


@app.route("/")
@app.route("/home")
def home():
    # Take the template in templates and show it
    return render_template("home.html")

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    # Post when press submit button
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # session is like a python dico specific to the user and accessible every where in the back end
        session["username"] = username
        return redirect(url_for("user_page"))
    else:
        # if already have a session -> go to user page
        if "username" in session:
            return redirect(url_for("user_page"))
        return render_template("sign_in.html")

@app.route("/user_page")
def user_page():
    if "username" in session:
        username = session["username"]
        # Pass the username in argument to recover and display it on the page, we can do it with list for
        # the favorit meal of the user
        return render_template("user_page.html", user = username)
    else:
        # no session -> go to sign in
        return redirect(url_for("sign_in"))

@app.route("/account_creation", methods=["POST", "GET"])
def account_creation():
    if request.method == "POST":
        print("Account")
        username = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("sign_in"))
    return render_template("account_creation.html")

@app.route("/foodstuffs_selection")
def foodstuffs_selection():
    data = pd.read_csv('nutrients_csvfile.csv')
    list_food_stucks = []
    for index, row in data.iterrows():
        list_food_stucks.append({'label':row['Food'], 'image_link':url_for('static', filename='images/Default_image.png')})
    # list_food_stucks = [{'label':"Tomato", 'image_link':"https://img.freepik.com/vecteurs-libre/tomates-fraiches_1053-566.jpg?w=740&t=st=1715677134~exp=1715677734~hmac=8d8bd9c4ab06aad73268c77d7ad362ce392f8fc6df666bb9ddd0a342f7850348"},
    #                     {'label':"Potato",'image_link':"https://lesrecoltesmarcotteboutique.com/cdn/shop/products/shutterstock_1073870363_600x.jpg?v=1587143918"},
    #                     {'label':"Beens", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Banana", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Maize", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Stawberry", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Ketchup", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Salad", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Porc", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Veau", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Poisson", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Chocapic", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Durum", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':'Pate', 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Fromage", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Tartine", 'image_link':url_for('static', filename='images/Default_image.png')},
    #                     {'label':"Brocoli", 'image_link':url_for('static', filename='images/Default_image.png')}]
    return render_template("foodstuffs_selection.html", list_food_stucks = list_food_stucks)

@app.route("/meal_resume", methods=["POST", "GET"])
def meal_resume():
    if request.method == "POST":
        data = request.get_json()
        print("Données reçues : ", data)

        # Réponse en JSON
        response = {
            'message': 'Données reçues avec succès',
            'received_data': data
        }
        return jsonify(response)
    if ("username" in session):
        return render_template("meal_resume.html", haveSession=True)
    return render_template("meal_resume.html", haveSession=False)

@app.route("/log_out")
def log_out():
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__=="__main__":
    app.run(debug=True)
