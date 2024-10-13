# dashboard/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Farm', 'Farm'),
        ('Processing', 'Processing'),
        ('Distribution', 'Distribution'),
        ('Retail', 'Retail'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select)

    class Meta:
        model = Product
        fields = ['name', 'description', 'status', 'certificate_image']
