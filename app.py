from flask import Flask, request
from flask_jwt_extended import JWTManager
from database import books_collection
from auth import auth
from flask_jwt_extended import jwt_required
from models import Book, User
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["JWT_SECRET_KEY"] = "mi-clave-secreta-123"
jwt = JWTManager(app)
app.register_blueprint(auth)

@app.route("/books", methods=["GET"])
def get_books():
    books = list(books_collection.find({}, {"_id": 0}))
    return books

@app.route("/books/<title>", methods=["GET"])
def get_book(title):
    book = books_collection.find_one({"title": title}, {"_id": 0})
    if book:
        return book
    return {"error": "Book not found"}, 404

@app.route("/books", methods=["POST"])
@jwt_required()
def create_book():
    try:
        new_book = request.get_json()
        book = Book(**new_book)
        books_collection.insert_one(book.model_dump())
        return book.model_dump(), 201
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error":str(e)}, 400

@app.route("/books/<title>", methods=["PUT"])
def update_book(title):
    data = request.get_json()
    books_collection.update_one({"title": title}, {"$set": data})
    book = books_collection.find_one({"title": title}, {"_id": 0})
    if book:
        return book, 200
    return {"error": "Book not found"}, 404

@app.route("/books/<title>", methods=["DELETE"])
def delete_book(title):
    print(f"Trying to delete: '{title}'")
    result = books_collection.delete_one({"title": title})
    if result.deleted_count > 0:
        return {"message": "Book deleted"}, 200
    return {"error": "Book not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)