import httpx

BASE_URL = "https://openlibrary.org/api/books"

async def get_book_info_by_isbn(isbn: str):
    params = {
        "bibkeys": f"ISBN:{isbn}",
        "format": "json",
        "jscmd": "data"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    
    book_key = f"ISBN:{isbn}"
    book_data = data.get(book_key)

    if not book_data:
        return None

    return {
        "title": book_data.get("title"),
        "authors": [author["name"] for author in book_data.get("authors", [])],
        "publish_date": book_data.get("publish_date"),
        "cover_url": book_data.get("cover", {}).get("medium")
    }