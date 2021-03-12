from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/accounts/login/"
    template_name = "signup.html"
