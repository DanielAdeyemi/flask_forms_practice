from sqlite3.dbapi2 import Cursor
from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired, DataRequired, Length
import sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

class ItemForm(FlaskForm):
  title = StringField("Title", validators=[InputRequired("Title is required"), DataRequired("No empty tricks!"), Length(min=2, max=20, message="Title should be between 2 and 20 charachters long")])
  price = FloatField("Price")
  description = TextAreaField("Description", validators=[InputRequired("Title is required"), DataRequired(
      "No empty tricks!"), Length(min=5, max=40, message="Title should be between 5 and 40 charachters long")])
  
class NewItemForm(ItemForm):
  category = SelectField("Category", coerce=int)
  subcategory = SelectField("Subcategory", coerce=int)
  submit = SubmitField("Submit")

class DeleteItemForm(FlaskForm):
  submit = SubmitField("Delete item")

class EditItemForm(ItemForm):
  submit = SubmitField("Update Item")


@app.route("/")
def home():
  conn = get_db()
  c = conn.cursor()

  items_from_db = c.execute("""SELECT 
                  i.id, i.title, i.description, i.price, i.image, c.name, s.name
                  FROM
                  items AS i
                  INNER JOIN categories AS c ON i.category_id = c.id
                  INNER JOIN subcategories AS s ON i.subcategory_id = s.id
                  ORDER BY i.id DESC
  """)

  items = []
  for row in items_from_db:
    item = {
      "id": row[0],
      "title": row[1],
      "description": row[2],
      "price": row[3],
      "image": row[4],
      "category": row[5],
      "subcategory": row[6]
    }
    items.append(item)
  return render_template("index.html", items=items)

@app.route("/item/new", methods=["GET", "POST"])
def new_item():
  conn = get_db()
  c = conn.cursor()
  form = NewItemForm()
  c.execute("SELECT id, name FROM categories")
  categories = c.fetchall()
  form.category.choices = categories

  c.execute("""SELECT id, name FROM subcategories WHERE category_id = ?""", (1,))
  subcategories = c.fetchall()
  form.subcategory.choices = subcategories

  if form.validate_on_submit():
    c.execute("""INSERT INTO items(title, description, price, image, category_id, subcategory_id) VALUES(?,?,?,?,?,?)""", 
              (form.title.data,
              form.description.data,
              form.price.data,
              "",
              form.category.data,
              form.subcategory.data
              ))
    conn.commit()
    flash("Item {} has been successfully created".format(request.form.get("title")), "success")
    return redirect(url_for("home"))
  
  if form.errors:
    flash(" {} ".format(form.errors), "danger")
  return render_template("new_item.html", form=form)

@app.route("/item/<item_id>")
def item(item_id):
  c = get_db().cursor()
  item_from_db = c.execute("""SELECT 
                i.id, i.title, i.description, i.price, i.image, c.name, s.name
                FROM
                items as i
                INNER JOIN categories AS c ON i.category_id = c.id
                INNER JOIN subcategories AS s ON i.subcategory_id = s.id
                WHERE i.id = ?""",
                (item_id))
  row = c.fetchone()
  try:
    item = {
      "id": row[0],
      "title": row[1],
      "description": row[2],
      "price": row[3],
      "image": row[4],
      "category": row[5],
      "subcategory": row[6]
    }
  except:
    item = {}
  
  if item:
    deleteItemForm = DeleteItemForm()
    return render_template("item.html", item=item, deleteItemForm=deleteItemForm)
  return redirect(url_for("home"))

@app.route("/item/<item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
  conn = get_db()
  c = conn.cursor()
  item_from_db = c.execute("SELECT * FROM items WHERE id = ?", (item_id))
  row = c.fetchone()
  try:
    item = {
      "id": row[0],
      "title": row[1],
      "description": row[2],
      "price": row[3],
      "image": row[4]
    }
  except:
    item = {}
  if item:
    form = EditItemForm()
    if form.validate_on_submit():
      c.execute("""UPDATE items SET
                title = ?, description = ?, price = ?
                WHERE id = ?""",
                (
                  form.title.data,
                  form.description.data,
                  form.price.data,
                  item_id
                ))
      conn.commit()
      flash("Item {} has been updated".format(form.title.data), "success")
      return redirect(url_for("item", item_id=item_id))

  form.title.data = item["title"]
  form.description.data = item["description"]
  form.price.data = item["price"]
  if form.errors:
    flash("{}".format(form.errors), "danger")
  return render_template("edit_item.html", item=item, form=form)
  
  return redirect(url_for("home"))

@app.route("/item/<item_id>/delete", methods=["POST"])
def delete_item(item_id):
  conn = get_db()
  c = conn.cursor()
  item_from_db = c.execute("SELECT * FROM items WHERE id = ?", (item_id))
  row = c.fetchone()
  try:
    item = {
      "id": row[0],
      "title": row[1]
    }
  except:
    item = {}
  if item:
    c.execute("DELETE FROM items WHERE id = ?", (item_id))
    conn.commit()
    flash("Item {} has been successfully deleted".format(item["title"]), "success")
  else:
    flash("This item doesn't exist", "danger")

  return redirect(url_for("home"))


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
