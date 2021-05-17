from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/item/new", methods=["GET", "POST"])
def new_item():
  if request.method == "POST":
    return redirect(url_for("home"))
  return render_template("new_item.html")