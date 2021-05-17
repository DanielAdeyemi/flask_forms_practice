from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/item/new", methods=["GET", "POST"])
def new_item():
  conn = get_db()
  c = conn.cursor()
  if request.method == "POST":
    return redirect(url_for("home"))
  return render_template("new_item.html")

def get_db():
  db = getattr(g, "_database", None)
  if db is None:
    g._database = sqlite3.connect("db/globomantics.db")
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, "_database", None)
  if db is not None:
    db.close()