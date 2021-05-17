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
    c.execute("""INSERT INTO items(title, description, price, image, category_id, subcategory_id) VALUES(?,?,?,?,?,?)""", 
              (request.form.get("title"),
              request.form.get("description"),
              float(request.form.get("price")),
              "",
              1,
              1
              ))
    conn.commit()
    return redirect(url_for("home"))
  return render_template("new_item.html")

def get_db():
  db = getattr(g, "_database", None)
  if db is None:
    db = g._database = sqlite3.connect("db/globomantics.db")
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, "_database", None)
  if db is not None:
    db.close()