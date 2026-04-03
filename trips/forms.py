from django import forms
from django.forms import inlineformset_factory
from .models import Trip, TripItem


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = [
            "title",
            "destination",
            "description",
            "start_date",
            "end_date",
            "story_title",
            "story_description",         
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

    class Meta:
        model = TripItem
        fields = [
            "title",
            "description",
            "user_note",
            "category",
            "story_title",
            "story_description",
            "date",
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


TripItemFormSet = inlineformset_factory(
    Trip,
    TripItem,
    form=TripItemForm,
    extra=3,
    can_delete=True
)