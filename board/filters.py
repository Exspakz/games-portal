from django.forms import DateInput, CheckboxInput

import django_filters
from django_filters import FilterSet

from .models import Post, Comment


class CommentFilter(FilterSet):
    date = django_filters.DateFilter(
        field_name='date_creation',
        lookup_expr='gt',
        label='Date',
        widget=DateInput(
            attrs={'type': 'date'},
        ),
    )

    post = django_filters.ModelChoiceFilter(
        field_name='post',
        queryset=None,
        label='Post',
        empty_label='Select a post',
    )

    accept = django_filters.BooleanFilter(
        field_name='is_accept',
        label='Accepted comments',
        widget=CheckboxInput()
    )

