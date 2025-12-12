from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


def default_due_date():
    return timezone.now().date() + timedelta(days=14)


class User(AbstractUser):
    """Custom user allowing flag for staff librarians."""

    is_librarian = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.get_full_name() or self.username


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    page_count = models.PositiveIntegerField(default=0)
    published_year = models.PositiveIntegerField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    available_copies = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    @property
    def is_available(self) -> bool:
        return self.available_copies > 0

    def clean_inventory(self):
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies

    def save(self, *args, **kwargs):
        self.clean_inventory()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"


class Loan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=default_due_date)
    returned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-borrowed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                condition=Q(returned_at__isnull=True),
                name="unique_active_loan",
            )
        ]

    @property
    def is_returned(self) -> bool:
        return self.returned_at is not None

    def mark_returned(self):
        self.returned_at = timezone.now()
        self.save(update_fields=["returned_at"])

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
