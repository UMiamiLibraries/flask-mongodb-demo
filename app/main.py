import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from forms import BookForm

app = Flask(__name__)
# NEVER store your secret key in version control!!!!
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')  # Change this to a random secret key
csrf = CSRFProtect(app)

client = MongoClient('mongodb://mongo:27017/')
db = client.library_db

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books')
def books():
    books = list(db.books.find())
    return render_template('books.html', books=books)

@app.route('/book/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = {
            'title': form.title.data,
            'author': form.author.data,
            'isbn': form.isbn.data,
            'published_year': form.published_year.data,
            'genre': form.genre.data
        }
        db.books.insert_one(book)
        flash('Book added successfully!', 'success')
        return redirect(url_for('books'))
    return render_template('book_form.html', form=form, title="Add Book")

@app.route('/book/edit/<string:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = db.books.find_one({'_id': ObjectId(id)})
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('books'))

    form = BookForm(obj=book)
    if form.validate_on_submit():
        updated_book = {
            'title': form.title.data,
            'author': form.author.data,
            'isbn': form.isbn.data,
            'published_year': form.published_year.data,
            'genre': form.genre.data
        }
        db.books.update_one({'_id': ObjectId(id)}, {'$set': updated_book})
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books'))

    # Pre-populate the form fields
    form.title.data = book['title']
    form.author.data = book['author']
    form.isbn.data = book['isbn']
    form.published_year.data = book['published_year']
    form.genre.data = book['genre']

    return render_template('book_form.html', form=form, title="Edit Book")


@app.route('/book/delete/<string:id>', methods=['POST'])
def delete_book(id):
    db.books.delete_one({'_id': ObjectId(id)})
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('books'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')