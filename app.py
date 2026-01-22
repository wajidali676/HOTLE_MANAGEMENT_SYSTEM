from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hotel_secret_key"

ROOM_PER_DAY = 3000
ROOM_PER_MONTH = 80000

MEAL_PRICES = {
    "1": 500,
    "2": 900,
    "3": 1200
}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        days = int(request.form["days"])
        meals = request.form["meals"]

        if days >= 30:
            room_cost = ROOM_PER_MONTH
        else:
            room_cost = days * ROOM_PER_DAY

        meal_cost = MEAL_PRICES[meals] * days
        total = room_cost + meal_cost

        session["summary"] = {
            "name": name,
            "days": days,
            "room_cost": room_cost,
            "meal_cost": meal_cost,
            "total": total
        }

        return redirect(url_for("summary"))

    return render_template(
        "booking.html",
        day_price=ROOM_PER_DAY,
        month_price=ROOM_PER_MONTH
    )


@app.route("/summary")
def summary():
    return render_template("summary.html", data=session.get("summary"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
