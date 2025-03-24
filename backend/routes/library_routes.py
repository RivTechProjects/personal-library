from flask import Blueprint, request, jsonify
from services.library_service import (
    add_book,
    get_books,
    is_book_in_library,
    update_book_status,
)

library_bp = Blueprint("library", __name__)

@library_bp.route("/api/add_book", methods=["POST"])
def add_book_endpoint():
    """
    Add a book to the library.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")
    authors = data.get("authors")
    description = data.get("description")
    cover_art = data.get("cover_art")

    if not title or not authors or not description:
        return jsonify({"error": "Title, authors, and description are required"}), 400

    try:
        add_book(title, ", ".join(authors), description, cover_art)
        return jsonify({"message": f"Book '{title}' added to your library!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@library_bp.route("/api/get_books", methods=["GET"])
def get_books_endpoint():
    """
    Retrieve all books from the library.
    """
    try:
        books = get_books()
        return jsonify([dict(book) for book in books])  # Convert SQLite Row objects to dictionaries
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@library_bp.route("/api/is_book_in_library", methods=["GET"])
def is_book_in_library_endpoint():
    """
    Check if a book exists in the library by title.
    """
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Title query parameter is required"}), 400

    try:
        book = is_book_in_library(title)
        if book:
            return jsonify({"exists": True, "book": dict(book)})
        else:
            return jsonify({"exists": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@library_bp.route("/api/update_book_status", methods=["PUT"])
def update_book_status_endpoint():
    """
    Update the reading status of a book in the library.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")
    status = data.get("status")

    if not title or not status:
        return jsonify({"error": "Title and status are required"}), 400

    try:
        update_book_status(title, status)
        return jsonify({"message": f"Updated the status of '{title}' to '{status}'."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500