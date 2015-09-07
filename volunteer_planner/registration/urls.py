"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""
from .views import RegistrationView, ActivationView, reg_complete, reg_act_complete

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^password/change/$',
                           auth_views.password_change,
                           name='password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='password_reset'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='password_reset_done'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='password_reset_complete'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='password_reset_confirm'),
                       url(r'^registration/$',
                           RegistrationView.as_view(),
                           {'template_name': 'registration_form.html'},
                           name='registation'),
                       url(r'^activate/$',
                           ActivationView.as_view(),
                           name='user_activate'),
                       url(r'^login/$',
                           'django.contrib.auth.views.login',
                           {'template_name': 'login.html'},
                           name='auth_login'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'template_name': 'logout.html'},
                           name='auth_logout'),
                       url(r'^registration_complete/$',
                           reg_complete, name="registration_complete"),
                       url(r'^registration_activation_complete/$',
                           reg_act_complete, name="registration_activation_complete"),
                       )
