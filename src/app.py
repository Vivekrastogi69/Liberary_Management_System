from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import library as lib

app = Flask(__name__, static_folder="../public", static_url_path="")
CORS(app)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ── Stats ────────────────────────────────────────────────────────────────────
@app.route("/api/stats")
def stats():
    return jsonify(lib.get_stats())


# ── Books ────────────────────────────────────────────────────────────────────
@app.route("/api/books", methods=["GET"])
def get_books():
    q = request.args.get("q", "").strip()
    books = lib.search_books(q) if q else lib.list_books()
    return jsonify(books)


@app.route("/api/books", methods=["POST"])
def post_book():
    body = request.json
    book = lib.add_book(body["title"], body["author"], int(body["copies"]))
    return jsonify(book), 201


@app.route("/api/books/<book_id>", methods=["DELETE"])
def del_book(book_id):
    ok = lib.delete_book(book_id)
    return jsonify({"ok": ok}), (200 if ok else 404)


# ── Members ──────────────────────────────────────────────────────────────────
@app.route("/api/members", methods=["GET"])
def get_members():
    return jsonify(lib.list_members())


@app.route("/api/members", methods=["POST"])
def post_member():
    body = request.json
    member = lib.add_member(body["name"], body["email"], body["phone"])
    return jsonify(member), 201


@app.route("/api/members/<member_id>", methods=["DELETE"])
def del_member(member_id):
    ok = lib.delete_member(member_id)
    return jsonify({"ok": ok}), (200 if ok else 404)


# ── Borrow / Return ──────────────────────────────────────────────────────────
@app.route("/api/borrow", methods=["POST"])
def borrow():
    body = request.json
    result = lib.borrow_book(body["member_id"], body["book_id"])
    return jsonify(result), (200 if result["ok"] else 400)


@app.route("/api/return", methods=["POST"])
def return_():
    body = request.json
    result = lib.return_book(body["member_id"], body["book_id"])
    return jsonify(result), (200 if result["ok"] else 400)


if __name__ == "__main__":
    print("\n📚  Library Management System – by Vivek Rastogi")
    print("    Running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
