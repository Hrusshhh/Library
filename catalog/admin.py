from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Book, Loan, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Library", {"fields": ("is_librarian",)}),
    )
    list_display = ("username", "email", "is_staff", "is_librarian")
    list_filter = ("is_staff", "is_superuser", "is_librarian")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "isbn",
        "available_copies",
        "total_copies",
        "is_available_status",
    )
    search_fields = ("title", "author", "isbn")
    list_filter = ("author",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(boolean=True, description="Available")
    def is_available_status(self, obj):
        return obj.is_available


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "book",
        "borrowed_at",
        "due_date",
        "returned_at",
        "is_returned_status",
    )
    search_fields = ("user__username", "book__title")
    list_filter = ("borrowed_at", "due_date", "returned_at")
    autocomplete_fields = ("user", "book")

    @admin.display(boolean=True, description="Returned")
    def is_returned_status(self, obj):
        return obj.is_returned
