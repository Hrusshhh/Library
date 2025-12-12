import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from catalog.models import Book, Loan

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client():
    def _client(user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    return _client


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="reader",
        password="readerpass123",
        email="reader@example.com",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        password="adminpass123",
        email="admin@example.com",
    )


@pytest.fixture
def book_factory(db):
    def _factory(**kwargs):
        defaults = {
            "title": "Sample Book",
            "author": "John Doe",
            "isbn": f"9780000000{Book.objects.count():03d}",
            "page_count": 100,
            "total_copies": 3,
            "available_copies": 3,
        }
        defaults.update(kwargs)
        return Book.objects.create(**defaults)

    return _factory


@pytest.fixture
def book(book_factory):
    return book_factory()


@pytest.fixture
def loan_factory(db, book_factory, user):
    def _factory(**kwargs):
        loan_user = kwargs.pop("user", user)
        loan_book = kwargs.pop("book", book_factory())
        loan = Loan.objects.create(user=loan_user, book=loan_book, **kwargs)
        if loan_book.available_copies > 0:
            loan_book.available_copies -= 1
            loan_book.save(update_fields=["available_copies"])
        return loan

    return _factory

