from pymongo import MongoClient
import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/librarydb')
client = MongoClient(MONGO_URI)
db = client['librarydb']

print('=== BOOKS COLLECTION ===')
books = list(db.books.find().limit(5))
if books:
    for book in books:
        print(f'ID: {book.get("id")}, Title: {book.get("title")}, Author: {book.get("author")}, Copies: {book.get("available_copies")}/{book.get("total_copies")}')
else:
    print('No books found')

print('\n=== MEMBERS COLLECTION ===')
members = list(db.members.find().limit(5))
if members:
    for member in members:
        print(f'ID: {member.get("id")}, Name: {member.get("name")}, Email: {member.get("email")}, Borrowed: {len(member.get("borrowed_books", []))}')
else:
    print('No members found')

print(f'\nDatabase: {db.name}')
print(f'Collections: {db.list_collection_names()}')