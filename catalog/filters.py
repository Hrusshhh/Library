import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    is_available = django_filters.BooleanFilter(method="filter_is_available")

    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "author": ["icontains"],
            "isbn": ["exact"],
        }

    def filter_is_available(self, queryset, name, value):
        if value is None:
            return queryset
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset.filter(available_copies=0)
