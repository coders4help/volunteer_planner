from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from volunteer_planner.utils import LoginRequiredMixin


@login_required()
def user_account_detail(request):
    user = request.user
    return render(request, 'user_detail.html', {'user': user})


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows a user to update their profile.
    """
    fields = ['first_name', 'last_name', 'email']
    template_name = "user_account_edit.html"
    success_url = reverse_lazy('account_detail')

    def get_object(self, queryset=None):
        return self.request.user