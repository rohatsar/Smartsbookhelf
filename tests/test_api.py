import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SmartBookShelf API çalışıyor"}

def test_add_and_get_book():
    isbn = "9780140328721"
    # Kitap ekle
    response = client.post(f"/books/?isbn={isbn}")
    assert response.status_code == 200
    data = response.json()
    assert "book" in data
    assert data["book"]["isbn"] == isbn

    # Eklenen kitabı al
    response = client.get(f"/books/{isbn}")
    assert response.status_code == 200
    book = response.json()
    assert book["isbn"] == isbn

def test_delete_book():
    isbn = "9780140328721"
    response = client.delete(f"/books/{isbn}")
    assert response.status_code == 200
    assert response.json()["message"] == "Kitap silindi"

    # Silindikten sonra bulunamaz
    response = client.get(f"/books/{isbn}")
    assert response.status_code == 404
