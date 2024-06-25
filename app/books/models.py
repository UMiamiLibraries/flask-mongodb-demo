from bson import ObjectId

class Book:
    def __init__(self, title, author, isbn, published_year, genre, _id=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.published_year = published_year
        self.genre = genre
        self._id = str(_id) if _id else None

    @staticmethod
    def from_dict(data):
        return Book(
            title=data.get('title'),
            author=data.get('author'),
            isbn=data.get('isbn'),
            published_year=data.get('published_year'),
            genre=data.get('genre'),
            _id=str(data.get('_id')) if data.get('_id') else None
        )

    def to_dict(self):
        book_dict = {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'published_year': self.published_year,
            'genre': self.genre,
        }
        if self._id:
            book_dict['_id'] = ObjectId(self._id)
        return book_dict

    def __repr__(self):
        return f"<Book {self.title} (ID: {self._id})>"