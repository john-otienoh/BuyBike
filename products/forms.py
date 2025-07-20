from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """Products Form"""

    class Meta:
        """Products Meta Form"""

        model = Product
        fields = "__all__"

    image = forms.ImageField(
        label="Product Image",
        required=False,
        widget=CustomClearableFileInput,
        help_text="Max 2MB. JPG or PNG only.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.active().only("id")

        base_attrs = {"class": "form-control rounded-1"}
        for field in self.fields.values():
            field.widget.attrs.update(base_attrs)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image too large (max 2MB)")
            if not image.name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise forms.ValidationError("Only JPG/PNG images allowed")
        return image
