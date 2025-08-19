import asyncio
from models.book import Book # type: ignore
from models.library import Library # type: ignore
from openlibrary_api import get_book_info_by_isbn  # type: ignore

def main():
    library = Library()

    while True:
        print("\n📚 Akıllı Kütüphane")
        print("1. ISBN ile Kitap Ekle (OpenLibrary API)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminiz: ")

        if choice == '1':
            isbn = input("ISBN: ")
            book_info = asyncio.run(get_book_info_by_isbn(isbn))
            if book_info:
                title = book_info['title']
                author = ", ".join(book_info['authors'])
                book = Book(title, author, isbn)
                library.add_book(book)
                print(f"✅ Kitap eklendi: {title} - {author}")
            else:
                print("⚠️ Kitap bulunamadı. Manuel giriş yap.")
                title = input("Kitap Adı: ")
                author = input("Yazar: ")
                book = Book(title, author, isbn)
                library.add_book(book)
                print("✅ Kitap manuel eklendi.")

        elif choice == '2':
            isbn = input("Silinecek Kitabın ISBN: ")
            library.remove_book(isbn)
            print("🗑️ Kitap silindi.")

        elif choice == '3':
            books = library.list_books()
            if books:
                print("\n📖 Kütüphanedeki Kitaplar:")
                for book in books:
                    print(book)
            else:
                print("🚫 Kütüphane boş.")

        elif choice == '4':
            isbn = input("Aranacak ISBN: ")
            book = library.find_book(isbn)
            if book:
                print("📘 Bulundu:", book)
            else:
                print("❌ Kitap bulunamadı.")

        elif choice == '5':
            print("Çıkılıyor...")
            break
        else:
            print("⚠️ Geçersiz seçim.")

if __name__ == "__main__":
    try:
        main()
    finally:
        library.close() # type: ignore