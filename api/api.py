from fastapi import FastAPI, HTTPException
from models.book import Book # type: ignore
from models.library import Library # type: ignore
from openlibrary_api import get_book_info_by_isbn # type: ignore
import asyncio
from fastapi import FastAPI

app = FastAPI()
library = Library()

@app.get("/")
def read_root():
    return {"message": "SmartBookShelf API çalışıyor"}

@app.post("/books/")
async def add_book_by_isbn(isbn: str):
    book_info = await get_book_info_by_isbn(isbn)
    if not book_info:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    
    book = Book(book_info['title'], ", ".join(book_info['authors']), isbn)
    library.add_book(book)
    return {"message": "Kitap eklendi", "book": book.to_dict()}

@app.get("/books/")
def list_books():
    books = library.list_books()
    return [book.to_dict() for book in books]

@app.get("/books/{isbn}")
def get_book(isbn: str):
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    return book.to_dict()

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    library.remove_book(isbn)
    return {"message": "Kitap silindi"}
