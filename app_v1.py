from flask import Flask, request
from database import books_collection
from bson import ObjectId

app = Flask(__name__)

books = [
    {"title": "book1", "author": "author1", "pages": 100, "available": True},
    {"title": "book2", "author": "author2", "pages": 200, "available": False},
    {"title": "book3", "author": "author3", "pages": 300, "available": True},
]

@app.route("/", methods=["GET"])
def home():
    return "Hello World!"

@app.route("/books", methods=["GET"])
def get_books():
    books = list(books_collection.find({},{"_id":0}))
    return books

@app.route("/books/<title>",methods=["GET"])
def get_book(title):
    for b in books:
        if b["title"] == title:
            return b
    return {"error,":"Book not found"}, 404

@app.route("/books", methods=["POST"])
def create_book():
    new_book = request.get_json()
    books_collection.insert_one(new_book)
    new_book.pop("_id")
    return new_book, 201

@app.route("/books/<title>",methods=["GET"])
def get_book(title):
    for b in books:
        if b["title"] == title:
            return b
    return {"error,":"Book not found"}, 404

@app.route("/books/<title>",methods=["PUT"])
def update_book(title):
    for b in books: 
        if b["title"] == title:
            data = request.get_json()
            b.update(data)
            return b, 200
    return {"error": "Book not found"}, 404

@app.route("/books/<title>",methods=["DELETE"])
def delete_book(title):
    for b in books:
        if b["title"] == title:
            books.remove(b)
            return {"message":"Book deleted"}, 200
    return {"error": "Book not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)

