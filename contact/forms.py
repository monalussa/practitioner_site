from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, label="Your name")
    email = forms.EmailField(label="Your email")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label="Message")
