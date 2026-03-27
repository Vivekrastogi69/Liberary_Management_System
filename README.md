# 📚 LibraVault — Library Management System

> A full-featured Library Management System with a beautiful web UI and a Python/Flask REST API backend.

**Developed by [Vivek Rastogi](https://github.com/your-username)**

---

## ✨ Features

- 📚 Add, view, search, and delete books
- 👥 Register and manage library members
- 🔄 Borrow and return books with availability tracking
- 📊 Live dashboard with key statistics
- 💾 Persistent MongoDB storage (local or cloud)
- 🎨 Beautiful, responsive dark-gold web UI

---

## 🗂️ Project Structure

```
library-management/
├── src/
│   ├── library.py       # Core library logic with MongoDB integration
│   └── app.py           # Flask REST API server
├── public/
│   └── index.html       # Single-page frontend UI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/library-management.git
cd library-management
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Set up MongoDB

**Option A: Local MongoDB**
- Install MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
- Start MongoDB service

**Option B: MongoDB Atlas (Cloud) - Recommended**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Create database user and whitelist your IP
4. Get connection string from "Connect" → "Connect your application"
5. Set environment variable: `MONGO_URI="your_atlas_connection_string"`

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python src/app.py
```

### 5. Open in browser

Visit **http://localhost:5000**

---

## 🛠️ API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/books` | List all books |
| GET | `/api/books?q=query` | Search books |
| POST | `/api/books` | Add a new book |
| DELETE | `/api/books/:id` | Delete a book |
| GET | `/api/members` | List all members |
| POST | `/api/members` | Add a new member |
| DELETE | `/api/members/:id` | Delete a member |
| POST | `/api/borrow` | Borrow a book |
| POST | `/api/return` | Return a book |

---

## 📦 Tech Stack

- **Backend:** Python 3, Flask, Flask-CORS
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Storage:** MongoDB (local or cloud)
- **Fonts:** Playfair Display + DM Sans (Google Fonts)

---

## 📸 Screenshots

> Dashboard, Books, Members, and Borrow/Return pages with a clean dark-gold editorial aesthetic.

---

## 👤 Author

**Vivek Rastogi**
- GitHub: [@your-username](https://github.com/your-username)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
