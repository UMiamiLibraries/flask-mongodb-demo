from flask import render_template, redirect, url_for, flash, request, current_app
from bson import ObjectId
from . import books
from .forms import BookForm
from .models import Book

@books.route('/')
def index():
    book_docs = list(current_app.db.books.find())
    print("Raw book documents:", book_docs)  # Debug print
    book_list = [Book.from_dict(book) for book in book_docs]
    print("Processed book list:", book_list)  # Debug print
    for book in book_list:
        print(f"Book ID: {book._id}, Title: {book.title}")  # Debug print
    return render_template('books/index.html', books=book_list)

@books.route('/add', methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            published_year=form.published_year.data,
            genre=form.genre.data
        )
        result = current_app.db.books.insert_one(book.to_dict())
        book._id = str(result.inserted_id)
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.index'))
    return render_template('books/form.html', form=form, title="Add Book")

@books.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    book_data = current_app.db.books.find_one({'_id': ObjectId(id)})
    if not book_data:
        flash('Book not found', 'error')
        return redirect(url_for('books.index'))

    book = Book.from_dict(book_data)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.published_year = form.published_year.data
        book.genre = form.genre.data
        current_app.db.books.update_one({'_id': ObjectId(id)}, {'$set': book.to_dict()})
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.index'))

    return render_template('books/form.html', form=form, title="Edit Book")

@books.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    current_app.db.books.delete_one({'_id': ObjectId(id)})
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('books.index'))