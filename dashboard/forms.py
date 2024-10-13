# dashboard/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[('Farm', 'Farm'), ('Processing', 'Processing'), ('Distribution', 'Distribution'), ('Retail', 'Retail')],
        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'status', 'certificate_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'rows': 3}),
            'certificate_image': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 border border-gray-300 rounded-md'}),
        }
