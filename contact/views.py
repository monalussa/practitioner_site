from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact:success")

    def form_valid(self, form):
        data = form.cleaned_data
        send_mail(
            subject=f"New enquiry from {data['name']}",
            message=f"Name: {data['name']}\nEmail: {data['email']}\n\n{data['message']}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "contact/success.html"
