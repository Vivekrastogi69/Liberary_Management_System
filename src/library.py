import os
import random
import string
from datetime import datetime

# ── MongoDB connection ────────────────────────────────
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/librarydb")
_client = MongoClient(MONGO_URI)
_db = _client["librarydb"]
books_col   = _db["books"]
members_col = _db["members"]


def _generate_id(prefix="B"):
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}-{suffix}"


# ── Books ─────────────────────────────────────────────

def add_book(title, author, copies):
    book = {
        "_id": _generate_id("B"),
        "id": _generate_id("B"),
        "title": title,
        "author": author,
        "total_copies": copies,
        "available_copies": copies,
        "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    book["_id"] = book["id"]
    books_col.insert_one(book)
    return _clean(book)

def list_books():
    return [_clean(b) for b in books_col.find()]

def search_books(query):
    q = query.lower()
    return [_clean(b) for b in books_col.find({
        "$or": [
            {"title":  {"$regex": q, "$options": "i"}},
            {"author": {"$regex": q, "$options": "i"}},
        ]
    })]

def delete_book(book_id):
    r = books_col.delete_one({"_id": book_id})
    return r.deleted_count > 0


# ── Members ───────────────────────────────────────────

def add_member(name, email, phone):
    member = {
        "id": _generate_id("M"),
        "name": name,
        "email": email,
        "phone": phone,
        "borrowed_books": [],
        "joined_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    member["_id"] = member["id"]
    members_col.insert_one(member)
    return _clean(member)

def list_members():
    return [_clean(m) for m in members_col.find()]

def delete_member(member_id):
    r = members_col.delete_one({"_id": member_id})
    return r.deleted_count > 0


# ── Borrow / Return ───────────────────────────────────

def borrow_book(member_id, book_id):
    member = members_col.find_one({"_id": member_id})
    if not member:
        return {"ok": False, "error": "Member not found"}

    book = books_col.find_one({"_id": book_id})
    if not book:
        return {"ok": False, "error": "Book not found"}

    if book["available_copies"] <= 0:
        return {"ok": False, "error": "No copies available"}

    already = any(e["book_id"] == book_id for e in member.get("borrowed_books", []))
    if already:
        return {"ok": False, "error": "Member already borrowed this book"}

    entry = {
        "book_id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "borrowed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    members_col.update_one(
        {"_id": member_id},
        {"$push": {"borrowed_books": entry}}
    )
    books_col.update_one(
        {"_id": book_id},
        {"$inc": {"available_copies": -1}}
    )
    return {"ok": True, "entry": entry}


def return_book(member_id, book_id):
    member = members_col.find_one({"_id": member_id})
    if not member:
        return {"ok": False, "error": "Member not found"}

    entry = next((e for e in member.get("borrowed_books", []) if e["book_id"] == book_id), None)
    if not entry:
        return {"ok": False, "error": "This member has not borrowed that book"}

    members_col.update_one(
        {"_id": member_id},
        {"$pull": {"borrowed_books": {"book_id": book_id}}}
    )
    books_col.update_one(
        {"_id": book_id},
        {"$inc": {"available_copies": 1}}
    )
    return {"ok": True}


# ── Stats ─────────────────────────────────────────────

def get_stats():
    all_books   = list(books_col.find())
    all_members = list(members_col.find())
    return {
        "total_books":      len(all_books),
        "total_copies":     sum(b.get("total_copies", 0) for b in all_books),
        "available_copies": sum(b.get("available_copies", 0) for b in all_books),
        "total_members":    len(all_members),
        "active_borrows":   sum(len(m.get("borrowed_books", [])) for m in all_members),
    }


# ── Internal helper ───────────────────────────────────

def _clean(doc):
    doc.pop("_id", None)
    return doc
