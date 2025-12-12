from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import BookFilter
from .models import Book, Loan
from .permissions import IsStaffOrLibrarian, is_librarian_user
from .serializers import BookSerializer, LoanSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    search_fields = ["title", "author", "isbn", "description"]
    ordering_fields = ["title", "author", "published_year", "created_at"]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsStaffOrLibrarian()]
        return super().get_permissions()

    def get_queryset(self):
        return Book.objects.all()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def borrow(self, request, pk=None):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=pk)
            if not book.is_available:
                return Response(
                    {"detail": "Book is currently unavailable."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if Loan.objects.filter(
                user=request.user, book=book, returned_at__isnull=True
            ).exists():
                return Response(
                    {"detail": "You already have an active loan for this book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            loan = Loan.objects.create(user=request.user, book=book)
            book.available_copies -= 1
            book.save(update_fields=["available_copies"])

        serializer = LoanSerializer(loan, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["post"],
        url_path="return",
        permission_classes=[IsAuthenticated],
    )
    def return_book(self, request, pk=None):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=pk)
            target_user = request.user

            user_id = request.data.get("user_id")
            if user_id and is_librarian_user(request.user):
                target_user = get_object_or_404(User, id=user_id)

            loan = (
                Loan.objects.select_for_update()
                .filter(book=book, user=target_user, returned_at__isnull=True)
                .first()
            )
            if not loan:
                return Response(
                    {"detail": "No active loan found for this user and book."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            loan.mark_returned()
            book.available_copies = min(book.available_copies + 1, book.total_copies)
            book.save(update_fields=["available_copies"])

        serializer = LoanSerializer(loan, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Loan.objects.none()

        queryset = Loan.objects.select_related("book", "user")
        if is_librarian_user(self.request.user):
            return queryset
        return queryset.filter(user=self.request.user)
