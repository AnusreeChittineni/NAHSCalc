import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, json, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from collections import OrderedDict


from helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///NAHSCalc.db")


# Initilaizes a dictionary to store GPA Scale
# Needed because db.execute posed problems when using the fetched level of the course in a variable
GPA_scale = {
    "A+": {"CP": 4.3, "Honors": 4.8, "AP": 5.3},
    "A": {"CP": 4.0, "Honors": 4.5, "AP": 5.0},
    "A-": {"CP": 3.7, "Honors": 4.2, "AP": 4.7},
    "B+": {"CP": 3.3, "Honors": 3.8, "AP": 4.3},
    "B": {"CP": 3.0, "Honors": 3.5, "AP": 4.0},
    "B-": {"CP": 2.7, "Honors": 3.2, "AP": 3.7},
    "C+": {"CP": 2.3, "Honors": 2.8, "AP": 3.3},
    "C": {"CP": 2.0, "Honors": 2.5, "AP": 3.0},
    "C-": {"CP": 1.7, "Honors": 2.2, "AP": 2.7},
    "D+": {"CP": 1.3, "Honors": 1.8, "AP": 2.3},
    "D": {"CP": 1.0, "Honors": 1.5, "AP": 2.0},
    "F": {"CP": 0.0, "Honors": 0.0, "AP": 0.0}
}

# Initializes a dictionary to store Grade Scale
Grade_scale = {
    "A+": 96.5, "A": 93.5, "A-": 89.5,
    "B+": 86.5, "B": 83.5, "B-": 79.5,
    "C+": 76.5, "C": 73.5, "C-": 69.5,
    "D+": 66.5, "D": 64.5
}


# HOMEPAGE
@app.route("/")
def Welcome():

    return render_template("welcome.html")


# GPA CALCULATOR
@app.route("/GPA_Calculator", methods=["GET", "POST"])
def GPA_Calculator():

    # Checks if method is POST; form was submitted
    if request.method == "POST":

        # Initializes variables to store values from last two fields of the form
        current_GPA = float(request.form.get("GPA"))
        class_count = float(request.form.get("class count"))

        # Initilaizes a varaible to store original class_count
        old_class_count = class_count

        # Initilaizes variable to store total GPA Scale numbers being added to GPA
        new_GPA = 0

        # Initializes an ordered dictionary to store submitted classes
        ordered_dict = OrderedDict(request.form)

        # Intializes an empty list to store GPA value for each class
        values = []

        # Loops through each item in ordered_dict to extract values
        for key, value in ordered_dict.items():

            values.append(value)

        # Pops last two values from values because they are the last two fields of the form, not classes
        values.pop(-1)
        values.pop(-1)

        # Loops through each value in values
        for value in range(len(values)-1):

            # Checks if the index value is even
            # Does this to group the values into pairs, because all the even values correspond to a course level, and the odd ones are the grade
            if value % 2 == 0:

                # increases class count by 1 for every loop through if statement
                class_count += 1

                # gets level for class
                level = values[value]

                # gets grade for class
                grade = values[value+1]

                # gets value from GPA Scale dictionary and adds to new_GPA
                new_GPA += GPA_scale[grade][level]

            # If index value is odd, skip iteration
            else:

                continue

        # Calculates GPA to the second decimal point, using formula
        GPA = round(((current_GPA * old_class_count) + new_GPA) / class_count, 3)

        # Returns template GPA.html to display GPA
        return render_template("GPA.html", GPA = GPA)

    # If method is not POST, then it is GET
    else:

        # Returns template GPA_calc.html, which has the GPA calculator form
        return render_template("GPA_calc.html")


# FINAL GRADE CALCULATOR
@app.route("/FinalGradeCalculator", methods=["GET", "POST"])
def FG_Calculator():

    # Checks if method is POST; form was submitted
    if request.method == "POST":

        # Initializes variables to store values the form
        current_grade = float(request.form.get("Current Grade"))

        desired_grade = request.form.get("Desired Grade")

        # Initializes a variable to store the numeric grade needed, gets value from Grade Scale dictionary
        minimum_grade = Grade_scale[desired_grade]


        final_grade_chart = dict()

        for key, value in Grade_scale.items():

            final_grade_chart[key] = (minimum_grade - 0.9*current_grade) / 0.1

            if key == desired_grade:

                final_grade = round(final_grade_chart[key],3)

        # Returns template FG.html to display Final Grade
        return render_template("FG.html", final_grade = final_grade, desired_grade = desired_grade)

    # If method is not POST, then it is GET
    else:

        # Returns template FG_calc.html, which has the Final Grade calculator form
        return render_template("FG_calc.html")


# GPA SCALE
@app.route("/GPA_Scale")
def gpa_scale():

    scale = db.execute("SELECT * FROM GPA_Scale")

    return render_template("gpa_scale.html", scale=scale)


# GRADE SCALE
@app.route("/Grade_Scale")
def grade_scale():

    scale = db.execute("SELECT * FROM Grade_Scale")

    return render_template("grade_scale.html", scale=scale)




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
