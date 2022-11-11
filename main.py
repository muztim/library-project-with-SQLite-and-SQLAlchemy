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
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()           # create a database

# db = sqlite3.connect('')
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
#                "NOT NULL, rating FLOAT NOT NULL) ")

# cursor.execute("INSERT INTO books VALUES(10, 'Who sold the Monks ferari', 'R. Sharma', '6')")
# db.commit()


# -------------- Create records ----------- #
# newbook = NewBook(title="Deep Work", author="C. Newport", rating=8.5)
# db.session.add(newbook)
# db.session.commit()

# -------------- CRUD records with SQLAlchemy ---------------#

# book_to_update = NewBook.query.filter_by(title="Harry Potter").first()   # how to read record
# # print(book_to_update)
# book_to_update.title = "Harry Potter and the Chamber of Secrets"     # update a record by query
# db.session.commit()

# book_id = 1
# book_to_update = NewBook.query.get(book_id)
# book_to_update.title = "Harry Potter and the Goblet of Fire"    # update a record by primary key
# db.session.commit()


# book_id = 10
# book_to_delete = NewBook.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()


@app.route('/')
def home():
    all_books = db.session.query(NewBook).all()
    print(all_books)
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_book = request.form.to_dict()
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        # update rating record
        book_id = request.form["id"]
        book_to_update = NewBook.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = NewBook.query.get(book_id)
    return render_template('edit_rating.html', book=book_selected)


@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    # delete a record by ID
    db.session.delete(book_id)
    db.session.commit()
    return render_template(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

