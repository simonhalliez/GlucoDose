from flask import Flask, redirect, url_for, render_template, request, session

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
        username = request.form["username"]
        password = request.form["password"]
    return render_template("account_creation.html")

@app.route("/foodstuffs_selection")
def foodstuffs_selection():
    return render_template("foodstuffs_selection.html")

@app.route("/meal_resume")
def meal_resume():
    if ("username" in session):
        return render_template("meal_resume.html", haveSession=True)
    return render_template("meal_resume.html", haveSession=False)

@app.route("/log_out")
def log_out():
    session.pop("username", None)
    return redirect(url_for("home"))


if __name__=="__main__":
    app.run(debug=True)
