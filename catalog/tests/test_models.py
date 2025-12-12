from django.contrib.auth import get_user_model
from django.utils import timezone

from catalog.models import Loan


def test_book_inventory_is_normalized(book_factory):
    book = book_factory(total_copies=2, available_copies=5)
    assert book.available_copies == 2
    assert book.is_available is True


def test_loan_mark_returned_updates_timestamp(loan_factory):
    loan = loan_factory()
    assert loan.returned_at is None
    loan.mark_returned()
    loan.refresh_from_db()
    assert loan.returned_at is not None
    assert loan.is_returned is True


def test_user_string_representation(db):
    user = get_user_model().objects.create_user(
        username="fullname",
        password="complexpass123",
        first_name="Jane",
        last_name="Reader",
    )
    assert str(user) == "Jane Reader"
