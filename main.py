from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)
db = sqlite3.connect('books-collection.bd')
cursor = db.cursor()
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
               "NOT NULL, rating FLOAT NOT NULL) ")


all_books = []
books = []
data_file = {}


@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        all_books.append(request.form.to_dict())
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

