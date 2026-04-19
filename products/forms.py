from django import forms
from .models import Review

class ProductSearchForm(forms.Form):
    q = forms.CharField(
        required=False, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search bikes, parts, gear...',
                'autocomplete': 'off',
            }
        )
    )

    category = forms.CharField(required=False, widget=forms.HiddenInput())
    min_price = forms.DecimalField(
        required=False, min_value=0, widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Min $'
            }
        )
    )
    max_price = forms.DecimalField(
        required=False, min_value=0, widget=forms.NumberInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Max $'
            }
        )
    )
    brand = forms.CharField(required=False, widget=forms.HiddenInput())
    bike_type = forms.CharField(required=False, widget=forms.HiddenInput())

    SORT_CHOICES = [
        ('', 'Relevance'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('newest', 'Newest'),
        ('rating', 'Top Rated'),
        ('popular', 'Most Popular'),
    ]
    sort = forms.ChoiceField(
        choices=SORT_CHOICES, required=False, widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        )
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'body']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                                   attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                          'placeholder': 'Share your experience...'}),
        }