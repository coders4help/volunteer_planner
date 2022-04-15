from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from organizations.admin import MembershipFieldListFilter, MembershipFilteredAdmin
from . import models


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = models.NewsEntry
        fields = "__all__"

    text = forms.CharField(widget=CKEditorWidget())


@admin.register(models.NewsEntry)
class NewsAdmin(MembershipFilteredAdmin):
    form = NewsAdminForm

    list_display = (
        "title",
        "subtitle",
        "slug",
        "creation_date",
        "facility",
        "organization",
    )
    list_filter = (
        ("facility", MembershipFieldListFilter),
        ("organization", MembershipFieldListFilter),
    )
    readonly_fields = ("slug",)
    search_fields = ("title", "subtitle")

    def get_queryset(self, request):
        return (
            super(NewsAdmin, self)
            .get_queryset(request)
            .select_related("organization", "facility")
            .prefetch_related("organization", "facility")
        )
