from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city']


class CheckoutForm(forms.Form):
    # Shipping
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    street_address = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apartment = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=100, initial='United States',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    # Coupon
    coupon_code = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Coupon code'}))

    SHIPPING_CHOICES = [
        ('standard', 'Standard Shipping (5-7 days) – Free'),
        ('express', 'Express Shipping (2-3 days) – $15.00'),
        ('overnight', 'Overnight (1 day) – $35.00'),
    ]
    shipping_method = forms.ChoiceField(
        choices=SHIPPING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='standard'
    )