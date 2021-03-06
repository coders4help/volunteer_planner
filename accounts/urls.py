# coding: utf-8

from django.conf.urls import url


from .views import user_account_detail, AccountUpdateView, AccountDeleteView, account_delete_final, shift_list_active, shift_list_done

urlpatterns = [
    url(r'^edit/$', AccountUpdateView.as_view(), name="account_edit"),
    url(r'^myshifts/$', shift_list_active, name="shift_list_active"),
    url(r'^myshiftsdone/$', shift_list_done, name="shift_list_done"),
    url(r'^delete/$', AccountDeleteView.as_view(), name="account_delete"),
    url(r'^delete_final/$', account_delete_final, name="account_delete_final"),
    url(r'^', user_account_detail, name="account_detail"),
]
