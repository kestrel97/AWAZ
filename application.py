import os

from cs50 import SQL, eprint
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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
db = SQL("sqlite:///awaz.db")

# look for it
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")

@app.route("/rindex")
@login_required
def rindex():
    """Show portfolio of stocks"""
    row = db.execute("SELECT username FROM represent WHERE id=:id",id=session["user_id"])
    return render_template("rindex.html",row = row)

@app.route("/cindex")
@login_required
def cindex():
    """Show portfolio of stocks"""
    row = db.execute("SELECT username FROM citizen WHERE id=:id",id=session["user_id"])
    # eprint(row[0]['username'])
    return render_template("cindex.html", row = row)


@app.route("/login", methods=["GET", "POST"])
def login():
    """open Log in page"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via get)
    if request.method == "GET":
        return render_template("login.html")


@app.route("/rlogin", methods=["GET", "POST"])
def rlogin():
    """Log representative in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM represent WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/rindex")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/clogin", methods=["GET", "POST"])
def clogin():
    """Log citizen in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM citizen WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/cindex")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")


@app.route("/rregister", methods=["GET", "POST"])
def rregister():
    """Register representative"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation failed", 400)


        names = db.execute("select username from represent")
        # eprint(names)
        for nm in names:
            if request.form.get("username") == nm['username']:
                return apology("username taken", 400)

        pwhash = generate_password_hash(request.form.get("password"))
        # eprint(pw_hash)
        rows = db.execute("INSERT INTO represent (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=pwhash)


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/cregister", methods=["GET", "POST"])
def cregister():
    """Register citizen"""
        # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation failed", 400)


        names = db.execute("select username from citizen")
        # eprint(names)
        for nm in names:
            if request.form.get("username") == nm['username']:
                return apology("username taken", 400)

        pwhash = generate_password_hash(request.form.get("password"))
        # eprint(pw_hash)
        rows = db.execute("INSERT INTO citizen (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=pwhash)


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/complaint", methods=["GET", "POST"])
@login_required
def complaint():
    """let the user register a complaint """

    if request.method == "POST":

        db.execute("INSERT INTO complaints (name, email, na, pa, complaint, u_id) VALUES(:name, :email, :na, :pa, :complaint, :uid)",
            name = request.form.get("name"), email =  request.form.get("email"), na = request.form.get("na"), pa = request.form.get("pa"),complaint = request.form.get("complaint"), uid = session["user_id"])



        return redirect("/cindex")

    else:
        return render_template("complaint.html")


@app.route("/previous", methods=["GET", "POST"])
@login_required
def previous():
    """open user's previous complaints"""

    if request.method == "GET":
        rows = db.execute("SELECT  id, na, pa, complaint, time, notice, resolve FROM complaints WHERE u_id=:uid ",uid=session["user_id"])
        return render_template("previous.html", rows = rows )

@app.route("/show", methods=["GET", "POST"])
@login_required
def show():
    """show complaints to the representative"""

    if request.method == "POST":
        napa = request.form.get("napa")

        if napa == "na":
            rows = db.execute("SELECT id, name, complaint, time FROM complaints WHERE na=:num AND resolve='0' ",
                num=request.form.get("number"))
        else:
            rows = db.execute("SELECT id, name, complaint, time, notice FROM complaints WHERE pa=:num AND resolve='0' ",
                num=request.form.get("number"))

        return render_template("show.html",rows = rows)


@app.route("/notice", methods=["GET", "POST"])
@login_required
def notice():
    db.execute("UPDATE complaints SET notice = '1' WHERE id = :iid",iid = request.args.get("id"))
    return jsonify()

@app.route("/resolve", methods=["GET", "POST"])
@login_required
def resolve():
    db.execute("UPDATE complaints SET resolve = '1' WHERE id = :iid",iid = request.args.get("id"))
    return jsonify()


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
