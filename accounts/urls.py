from django.conf.urls import url
from .views import user_account_detail, AccountUpdateView

urlpatterns = [
    url(r'^edit/$', AccountUpdateView.as_view(), name="account_edit"),
    url(r'^', user_account_detail, name="account_detail"),
]
