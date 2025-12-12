from django.contrib.auth import get_user_model


def test_anonymous_user_can_list_books(api_client, book):
    response = api_client.get("/api/books/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == book.title


def test_authenticated_user_can_borrow_book(auth_client, user, book):
    client = auth_client(user)
    response = client.post(f"/api/books/{book.id}/borrow/")
    assert response.status_code == 201
    book.refresh_from_db()
    assert book.available_copies == 2


def test_user_cannot_borrow_same_book_twice(auth_client, user, book):
    client = auth_client(user)
    first = client.post(f"/api/books/{book.id}/borrow/")
    assert first.status_code == 201
    second = client.post(f"/api/books/{book.id}/borrow/")
    assert second.status_code == 400


def test_user_can_return_book(auth_client, user, book):
    client = auth_client(user)
    borrow = client.post(f"/api/books/{book.id}/borrow/")
    assert borrow.status_code == 201
    response = client.post(f"/api/books/{book.id}/return/")
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.available_copies == 3


def test_admin_can_create_book(auth_client, admin_user):
    client = auth_client(admin_user)
    payload = {
        "title": "Admin Created",
        "author": "Librarian",
        "isbn": "9789999999999",
        "page_count": 250,
        "total_copies": 5,
        "available_copies": 5,
    }
    response = client.post("/api/books/", payload, format="json")
    assert response.status_code == 201
    assert response.data["title"] == payload["title"]


def test_registration_endpoint_creates_user(api_client, db):
    payload = {
        "username": "apiuser",
        "email": "apiuser@example.com",
        "password": "StrongPass123",
    }
    response = api_client.post("/api/auth/register/", payload)
    assert response.status_code == 201
    assert response.data["username"] == payload["username"]


def test_jwt_token_generation(api_client, user):
    payload = {"username": user.username, "password": "readerpass123"}
    response = api_client.post("/api/auth/token/", payload)
    assert response.status_code == 200
    assert "access" in response.data and "refresh" in response.data


def test_user_sees_only_own_loans(auth_client, user, loan_factory):
    other_user = get_user_model().objects.create_user(
        username="other",
        password="otherpass123",
    )
    loan_factory(user=other_user)
    loan_factory(user=user)
    client = auth_client(user)
    response = client.get("/api/loans/")
    assert response.status_code == 200
    assert response.data["count"] == 1


def test_book_filter_by_availability(api_client, book_factory):
    book_factory(available_copies=0, isbn="9781111111111")
    book_factory(available_copies=2, isbn="9782222222222")
    response = api_client.get("/api/books/?is_available=true")
    assert response.status_code == 200
    assert response.data["count"] == 1
