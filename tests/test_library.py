import pytest
from models.book import Book
from models.library import Library

@pytest.fixture
def library():
    return Library(db_path="tests/test_library.db")

def test_add_and_find_book(library):
    book = Book("Test Kitap", "Yazar", "1234567890")
    library.add_book(book)
    found = library.find_book("1234567890")
    assert found is not None
    assert found.title == "Test Kitap"

def test_remove_book(library):
    book = Book("Silinecek Kitap", "Yazar", "0987654321")
    library.add_book(book)
    library.remove_book("0987654321")
    assert library.find_book("0987654321") is None

def test_list_books(library):
    # Tüm kitapları temizle
    cursor = library.conn.cursor()
    cursor.execute("DELETE FROM books")
    library.conn.commit()

    book1 = Book("Kitap 1", "Yazar 1", "111")
    book2 = Book("Kitap 2", "Yazar 2", "222")
    library.add_book(book1)
    library.add_book(book2)
    books = library.list_books()
    assert len(books) == 2