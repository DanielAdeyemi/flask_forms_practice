from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/item/new")
def new_item():
  return render_template("new_item.html")