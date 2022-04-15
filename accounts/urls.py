from django.urls import re_path

from .views import (
    account_delete_final,
    AccountDeleteView,
    AccountUpdateView,
    shift_list_active,
    shift_list_done,
    user_account_detail,
)

urlpatterns = [
    re_path(r"^edit/$", AccountUpdateView.as_view(), name="account_edit"),
    re_path(r"^myshifts/$", shift_list_active, name="shift_list_active"),
    re_path(r"^myshiftsdone/$", shift_list_done, name="shift_list_done"),
    re_path(r"^delete/$", AccountDeleteView.as_view(), name="account_delete"),
    re_path(r"^delete_final/$", account_delete_final, name="account_delete_final"),
    re_path(r"^", user_account_detail, name="account_detail"),
]
