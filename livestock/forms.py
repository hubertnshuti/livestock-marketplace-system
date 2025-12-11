# livestock/forms.py

from django import forms
from .models import LivestockItem, LivestockSpecies, Breed
from .models import LivestockImage

class LivestockItemForm(forms.ModelForm):
    # Field to select the Species first
    species = forms.ModelChoiceField(
        queryset=LivestockSpecies.objects.all(),
        label="Select Species (e.g., Cattle, Goat)",
        empty_label="--- Select Species ---"
    )

    # Breed field will be populated via AJAX (we will handle this complexity later), 
    # but for now, we include all breeds and mark it optional.
    breed = forms.ModelChoiceField(
        queryset=Breed.objects.all(),
        label="Breed (Optional)",
        required=False,
        empty_label="--- Select Breed ---"
    )

    class Meta:
        model = LivestockItem
        fields = [
            'species', 'breed', 'tag_id', 'quantity', 'gender', 
            'age', 'weight', 'price', 'description', 'is_for_sale'
        ]
        widgets = {
            'tag_id': forms.TextInput(attrs={'placeholder': 'Optional IoT Tag ID'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price (RWF)'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detailed description and health notes...'}),
        }

class LivestockImageForm(forms.ModelForm):
    class Meta:
        model = LivestockImage
        fields = ['image']

class SimpleOrderForm(forms.Form):
    # Field for buyer to send a message
    inquiry_message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional: Ask about delivery or health records...'}),
        required=False
    )
    # Hidden field for quantity (defaults to 1)
    quantity = forms.IntegerField(initial=1, min_value=1, widget=forms.HiddenInput())