import streamlit as st
import json
import os
from datetime import datetime

# --- Correct Banner Image URL from GitHub (Raw format) ---
BANNER_IMAGE_URL = "https://raw.githubusercontent.com/hoorain17/Book-and-Quote-Collector/main/image/banner.jpg"

# --- File Paths ---
BOOKS_FILE = "data/books.json"
QUOTES_FILE = "data/quotes.json"

# --- Ensure folders exist ---
def initialize_data_directory():
    os.makedirs("data", exist_ok=True)

initialize_data_directory()

# --- Load Data ---
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_data(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# --- App Header with Image ---
st.image(BANNER_IMAGE_URL, use_container_width=True)

st.markdown("""
    <h1 style='text-align: center; color: #4B8BBE;'>📚 Book & Quote Journal</h1>
    <p style='text-align: center; color: gray;'>Track books you’ve read and collect quotes that inspire you.</p>
    <hr style='margin-top: 20px; margin-bottom: 40px;'>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
menu = st.sidebar.radio("📂 Navigate", [
    "📘 Add Book", "📖 View Books", "🔍 Search Books", 
    "✏️ Update Book", "🗑️ Delete Book", "📝 Add Quote", 
    "🔖 View Quotes", "🔍 Search Quotes", "🗑️ Delete Quote"
])

books = load_data(BOOKS_FILE)
quotes = load_data(QUOTES_FILE)

# --- Book Functions ---
def add_book_st(books):
    st.subheader("📘 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    date_read = st.date_input("Date Read")
    rating = st.slider("Rating", 1, 10, 5)

    if st.button("➕ Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "date_read": date_read.strftime('%Y-%m-%d'),
            "rating": rating
        }
        books.append(new_book)
        save_data(books, BOOKS_FILE)
        st.success("Book added successfully!")

def view_books_st(books):
    st.subheader("📖 All Books")
    if books:
        for book in books:
            st.markdown(f"**📗 {book.get('title', 'No Title')}** by {book.get('author', 'Unknown Author')} ({book.get('genre', 'Unknown')})")
            st.markdown(f"📅 Read on: {book.get('date_read', 'Unknown Date')} &nbsp; ⭐ Rating: {book.get('rating', 'N/A')}")
            st.markdown("---")
    else:
        st.info("No books found.")

def search_books_st(books):
    st.subheader("🔍 Search Books")
    query = st.text_input("Search by title, author, or genre")
    if query:
        results = [b for b in books if query.lower() in b['title'].lower() or
                   query.lower() in b['author'].lower() or
                   query.lower() in b['genre'].lower()]
        if results:
            for book in results:
                st.markdown(f"**📗 {book['title']}** by {book['author']} ({book['genre']})")
                st.markdown(f"📅 Read on: {book['date_read']} &nbsp; ⭐ Rating: {book['rating']}")
                st.markdown("---")
        else:
            st.warning("No matching books found.")

def update_book_st(books):
    st.subheader("✏️ Update Book")
    titles = [book["title"] for book in books]
    if not titles:
        st.info("No books to update.")
        return

    selected_title = st.selectbox("Select a Book", titles)
    selected_book = next(b for b in books if b["title"] == selected_title)

    title = st.text_input("Title", value=selected_book["title"])
    author = st.text_input("Author", value=selected_book["author"])
    genre = st.text_input("Genre", value=selected_book.get("genre", ""))

    date_read = st.date_input("Date Read", datetime.strptime(selected_book.get("date_read", datetime.today().strftime("%Y-%m-%d")), "%Y-%m-%d"))
    rating = st.slider("Rating", 1, 10, selected_book.get("rating", 5))

    if st.button("✅ Update Book"):
        selected_book.update({
            "title": title,
            "author": author,
            "genre": genre,
            "date_read": date_read.strftime("%Y-%m-%d"),
            "rating": rating
        })
        save_data(books, BOOKS_FILE)
        st.success("Book updated successfully.")

def delete_book_st(books):
    st.subheader("🗑️ Delete Book")
    titles = [book["title"] for book in books]
    if not titles:
        st.info("No books to delete.")
        return
    selected_title = st.selectbox("Select a Book to Delete", titles)
    if st.button("🗑️ Confirm Delete"):
        books = [b for b in books if b["title"] != selected_title]
        save_data(books, BOOKS_FILE)
        st.success("Book deleted successfully.")

# --- Quote Functions ---
def add_quote_st(books, quotes):
    st.subheader("📝 Add a Quote")
    book_titles = [book["title"] for book in books]
    if not book_titles:
        st.warning("Add a book first.")
        return
    book_title = st.selectbox("Select Book", book_titles)
    quote_text = st.text_area("Quote")
    if st.button("➕ Add Quote"):
        quotes.append({
            "book_title": book_title,
            "quote": quote_text,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_data(quotes, QUOTES_FILE)
        st.success("Quote added successfully!")

def view_quotes_st(quotes):
    st.subheader("🔖 All Quotes")
    if quotes:
        for q in quotes:
            st.markdown(f"📘 **{q.get('book_title', 'Unknown Book')}**")
            st.markdown(f"> _{q.get('quote', 'No quote available')}_")
            st.markdown(f"🕒 {q.get('timestamp', 'No timestamp available')}")
            st.markdown("---")
    else:
        st.info("No quotes found.")

def search_quotes_st(quotes):
    st.subheader("🔍 Search Quotes")
    query = st.text_input("Search quotes or book titles")
    if query:
        results = [q for q in quotes if query.lower() in q.get('quote', '').lower() or
                   query.lower() in q.get('book_title', '').lower()]
        if results:
            for q in results:
                st.markdown(f"📘 **{q['book_title']}**")
                st.markdown(f"> _{q['quote']}_")
                st.markdown(f"🕒 {q['timestamp']}")
                st.markdown("---")
        else:
            st.warning("No matching quotes found.")

def delete_quote_st(quotes):
    st.subheader("🗑️ Delete Quote")
    if not quotes:
        st.info("No quotes to delete.")
        return
    quote_choices = [f"{q.get('book_title', 'Unknown Book')}: {q.get('quote', '')[:30]}..." for q in quotes]
    selected = st.selectbox("Select a Quote", quote_choices)
    if st.button("🗑️ Confirm Delete"):
        index = quote_choices.index(selected)
        quotes.pop(index)
        save_data(quotes, QUOTES_FILE)
        st.success("Quote deleted successfully.")

# --- Route to Selected Section ---
if menu == "📘 Add Book":
    add_book_st(books)
elif menu == "📖 View Books":
    view_books_st(books)
elif menu == "🔍 Search Books":
    search_books_st(books)
elif menu == "✏️ Update Book":
    update_book_st(books)
elif menu == "🗑️ Delete Book":
    delete_book_st(books)
elif menu == "📝 Add Quote":
    add_quote_st(books, quotes)
elif menu == "🔖 View Quotes":
    view_quotes_st(quotes)
elif menu == "🔍 Search Quotes":
    search_quotes_st(quotes)
elif menu == "🗑️ Delete Quote":
    delete_quote_st(quotes)
