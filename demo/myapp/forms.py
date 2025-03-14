from django import forms
from .models import SaveTheDate
from myapp.models import SaveTheDate


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class WeddingBookingForm(forms.ModelForm):
    class Meta:
        model = SaveTheDate
        fields = ['couples_names', 'email', 'phone', 'wedding_date', 'venue', 'photography_style', 'budget', 'message']
        widgets = {
            'wedding_date': forms.DateInput(attrs={'type': 'date'}),
        }