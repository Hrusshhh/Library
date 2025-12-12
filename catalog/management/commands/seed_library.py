from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalog.models import Book, Loan


BOOK_DATA = [
    {
        "title": "Matilda",
        "author": "Roald Dahl",
        "isbn": "9780140328721",
        "description": "Classic children novel about a gifted girl.",
        "page_count": 240,
        "published_year": 1988,
        "total_copies": 5,
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andy Hunt, Dave Thomas",
        "isbn": "9780201616224",
        "description": "Software craftsmanship guide.",
        "page_count": 352,
        "published_year": 1999,
        "total_copies": 3,
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "description": "A handbook of agile software craftsmanship.",
        "page_count": 464,
        "published_year": 2008,
        "total_copies": 4,
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "9780060935467",
        "description": "Pulitzer Prize-winning novel.",
        "page_count": 336,
        "published_year": 1960,
        "total_copies": 6,
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "description": "Dystopian social science fiction novel and cautionary tale.",
        "page_count": 328,
        "published_year": 1949,
        "total_copies": 5,
    },
    {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "isbn": "9780060850524",
        "description": "Dystopian novel about a technologically advanced future society.",
        "page_count": 268,
        "published_year": 1932,
        "total_copies": 4,
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "isbn": "9780547928227",
        "description": "Fantasy novel and prelude to The Lord of the Rings.",
        "page_count": 320,
        "published_year": 1937,
        "total_copies": 7,
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "9780441013593",
        "description": "Epic science fiction saga set on the desert planet Arrakis.",
        "page_count": 896,
        "published_year": 1965,
        "total_copies": 6,
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "isbn": "9780316769488",
        "description": "Story of teenage angst and alienation.",
        "page_count": 277,
        "published_year": 1951,
        "total_copies": 5,
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "description": "Novel chronicling the Jazz Age and the American Dream.",
        "page_count": 180,
        "published_year": 1925,
        "total_copies": 4,
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "isbn": "9780062316097",
        "description": "Exploration of the history and impact of Homo sapiens.",
        "page_count": 512,
        "published_year": 2015,
        "total_copies": 5,
    },
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "isbn": "9780374533557",
        "description": "Insights into how the mind works and makes decisions.",
        "page_count": 512,
        "published_year": 2011,
        "total_copies": 4,
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "isbn": "9780061122415",
        "description": "Inspirational novel about following one's dreams.",
        "page_count": 208,
        "published_year": 1988,
        "total_copies": 6,
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "isbn": "9780756404741",
        "description": "Fantasy novel following Kvothe's journey.",
        "page_count": 662,
        "published_year": 2007,
        "total_copies": 5,
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "isbn": "9780399590504",
        "description": "Memoir about a woman who grew up in a survivalist family.",
        "page_count": 352,
        "published_year": 2018,
        "total_copies": 4,
    },
    {
        "title": "Shadows of Forgotten Ancestors",
        "author": "Mykhailo Kotsiubynsky",
        "isbn": "9789660305875",
        "description": "A poetic novella about Hutsul life and tragic love in the Carpathians.",
        "page_count": 176,
        "published_year": 1911,
        "total_copies": 5,
    },
    {
        "title": "Kobzar",
        "author": "Taras Shevchenko",
        "isbn": "9789662169871",
        "description": "Collected poetry from the most iconic Ukrainian writer.",
        "page_count": 720,
        "published_year": 1840,
        "total_copies": 6,
    },
    {
        "title": "Sweet Darusya",
        "author": "Maria Matios",
        "isbn": "9789660309637",
        "description": "A powerful drama about a woman's fate and the history of Bukovyna.",
        "page_count": 240,
        "published_year": 2004,
        "total_copies": 4,
    },
    {
        "title": "Notes of a Ukrainian Madman",
        "author": "Lina Kostenko",
        "isbn": "9789661410677",
        "description": "Satirical chronicle-style novel reflecting modern Ukraine.",
        "page_count": 300,
        "published_year": 2010,
        "total_copies": 5,
    },
]

REGULAR_USERS = [
    {
        "username": "reader1",
        "email": "reader1@example.com",
        "first_name": "Alice",
        "last_name": "Reader",
        "password": "Reader1pass!",
    },
    {
        "username": "reader2",
        "email": "reader2@example.com",
        "first_name": "Bob",
        "last_name": "Reader",
        "password": "Reader2pass!",
    },
]

LIBRARIANS = [
    {
        "username": "librarian1",
        "email": "lib1@example.com",
        "first_name": "Laura",
        "last_name": "Books",
        "password": "Lib1#pass",
        "is_staff": True,
        "is_librarian": True,
    },
    {
        "username": "librarian2",
        "email": "lib2@example.com",
        "first_name": "Mark",
        "last_name": "Stacks",
        "password": "Lib2#pass",
        "is_staff": True,
        "is_librarian": True,
    },
]

ACTIVE_LOANS = [
    {"username": "reader1", "isbn": "9780140328721"},
    {"username": "reader2", "isbn": "9780132350884"},
]

RETURNED_LOANS = [
    {"username": "reader1", "isbn": "9780201616224"},
    {"username": "reader2", "isbn": "9780060935467"},
]


class Command(BaseCommand):
    help = "Seed the database with mock users, books, and loan records."

    def handle(self, *args, **options):
        self.stdout.write("Seeding library data...")
        users = self._create_users()
        books = self._create_books()
        self._create_loans(users, books)
        self.stdout.write(self.style.SUCCESS("Mock library data created."))

    def _create_users(self):
        user_model = get_user_model()
        created_users = {}

        for payload in REGULAR_USERS + LIBRARIANS:
            username = payload["username"]
            defaults = {
                "email": payload.get("email", ""),
                "first_name": payload.get("first_name", ""),
                "last_name": payload.get("last_name", ""),
                "is_staff": payload.get("is_staff", False),
                "is_librarian": payload.get("is_librarian", False),
            }
            user, created = user_model.objects.get_or_create(
                username=username,
                defaults=defaults,
            )
            if created:
                user.set_password(payload["password"])
                user.save()
                self.stdout.write(f" - Created user {username}")
            else:
                self.stdout.write(f" - User {username} already exists")
            created_users[username] = user

        return created_users

    def _create_books(self):
        books = {}
        for payload in BOOK_DATA:
            isbn = payload["isbn"]
            defaults = payload.copy()
            defaults.setdefault("available_copies", payload["total_copies"])
            book, created = Book.objects.get_or_create(
                isbn=isbn, defaults=defaults
            )
            if not created:
                for field, value in defaults.items():
                    setattr(book, field, value)
                book.save()
                self.stdout.write(f" - Updated book {book.title}")
            else:
                self.stdout.write(f" - Created book {book.title}")
            books[isbn] = book
        return books

    def _create_loans(self, users, books):
        for spec in ACTIVE_LOANS:
            user = users.get(spec["username"])
            book = books.get(spec["isbn"])
            if not user or not book:
                continue
            existing = Loan.objects.filter(
                user=user, book=book, returned_at__isnull=True
            ).first()
            if existing:
                self.stdout.write(
                    f" - Active loan already exists for {user} -> {book}"
                )
                continue
            loan = Loan.objects.create(user=user, book=book)
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save(update_fields=["available_copies"])
            self.stdout.write(
                f" - Created active loan {user.username} -> {book.title}"
            )

        for spec in RETURNED_LOANS:
            user = users.get(spec["username"])
            book = books.get(spec["isbn"])
            if not user or not book:
                continue
            loan = Loan.objects.create(user=user, book=book)
            loan.mark_returned()
            self.stdout.write(
                f" - Created returned loan {user.username} -> {book.title}"
            )
