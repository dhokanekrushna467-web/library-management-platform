
import pytest
from database.db import db
from app.services.library_service import LibraryService


@pytest.fixture(autouse=True)
def run_around_tests():
    db.reset()
    yield
    db.reset()


def test_add_book_success():
    book = LibraryService.add_book(
        "B100",
        "Clean Code",
        "Robert C. Martin",
        "ISBN100",
        5
    )

    assert book["book_id"] == "B100"
    assert book["title"] == "Clean Code"
    assert book["available_copies"] == 5


def test_add_duplicate_book_raises_error():
    with pytest.raises(ValueError, match="already exists"):
        LibraryService.add_book(
            "B001",
            "Duplicate Book",
            "Test Author",
            "ISBN200",
            2
        )


def test_search_books():
    results = LibraryService.search_books("Cloud")

    assert len(results) > 0
    assert results[0]["book_id"] == "B001"

