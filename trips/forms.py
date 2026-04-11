from django import forms
from django.forms import inlineformset_factory
from .models import Trip, TripItem
from itineraries.models import Category


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = [
            "title",
            "destination",
            "description",
            "start_date",
            "end_date",      
        ]

        labels = {
            "title": "Trip title",
            "destination": "Where are you going?",
            "start_date": "Start date",
            "end_date": "End date",
            "description": "Tell us about this trip",
        }

        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class TripItemForm(forms.ModelForm):

    title = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("display_order")

    class Meta:
        model = TripItem
        fields = [
            "title",
            "description",
            "user_note",
            "category",
            "story_title",
            "story_description",
            "travel_date",
            "day_night",
            "weather",
            "latitude",
            "longitude",
            "display_order",
        ]

        labels = {
            "title": "Stop name",
            "description": "What makes this place special?",
            "user_note": "Your personal tip",
            "category": "Type of experience",
        }

        help_texts = {
            "description": "Describe why this stop is worth visiting.",
            "user_note": "Optional: add your own travel tip.",
        }

        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "user_note": forms.Textarea(attrs={"rows": 2}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "display_order": forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        story_title = cleaned_data.get("story_title")

        # Auto fallback
        if not title and story_title:
            cleaned_data["title"] = story_title

        return cleaned_data


TripItemFormSet = inlineformset_factory(
    Trip,
    TripItem,
    form=TripItemForm,
    extra=3,
    can_delete=True
)