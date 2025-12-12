from catalog.serializers import BookSerializer, RegisterSerializer


def test_register_serializer_creates_user(db):
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "strong-pass-123",
        "first_name": "New",
        "last_name": "User",
    }
    serializer = RegisterSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.username == payload["username"]
    assert user.check_password(payload["password"])


def test_book_serializer_reports_availability(book):
    serializer = BookSerializer(book)
    assert "is_available" in serializer.data
    assert serializer.data["is_available"] is True
