import sqlite3
from models.book import Book # type: ignore

class Library:
    def __init__(self, db_path="data/library.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False) 
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_book(self, book: Book):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO books (isbn, title, author) VALUES (?, ?, ?)
        """, (book.isbn, book.title, book.author))
        self.conn.commit()

    def remove_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        self.conn.commit()

    def list_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT isbn, title, author FROM books")
        rows = cursor.fetchall()
        return [Book(title=row[1], author=row[2], isbn=row[0]) for row in rows]

    def find_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute("SELECT isbn, title, author FROM books WHERE isbn = ?", (isbn,))
        row = cursor.fetchone()
        if row:
            return Book(title=row[1], author=row[2], isbn=row[0])
        return None

    def close(self):
        self.conn.close()
        
    def clear_books(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books")
        self.conn.commit()    
