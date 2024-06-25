from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongo', 27017)
db = client.library_db

print(f"Connected to database: {db.name}")  # Add this line

@app.route('/')
def hello():
    return "Hello, Librarians!"

@app.route('/books')
def get_books():
    books = list(db.books.find({}, {'_id': 0}))
    print(f"Found {len(books)} books")  # Add this line
    return jsonify(books)

@app.route('/books/count')
def get_book_count():
    count = db.books.count_documents({})
    print(f"Book count: {count}")  # Add this line
    return jsonify({"count": count})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')