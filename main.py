from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()            # --- get context when opening database --- #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app=app)


# ---------------- Create table using SQLAlchemy ---------------- #
class NewBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()

# -------------- Create records ----------- #
newbook = NewBook(title="Harry Potter", author="J. K. Rowling", rating=9.1)
db.session.add(newbook)
db.session.commit()


# db = sqlite3.connect('')
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
#                "NOT NULL, rating FLOAT NOT NULL) ")

# cursor.execute("INSERT INTO books VALUES(10, 'Who sold the Monks ferari', 'R. Sharma', '6')")
# db.commit()


@app.route('/')
def home():
    all_books = db.session.query(NewBook).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_book = request.form.to_dict()
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

