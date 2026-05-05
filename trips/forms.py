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
            "story_title",
            "story_description",
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
            # ✅ ADD THESE
            "story_title": forms.TextInput(attrs={
                "class": "form-control trip-story-title-input"
            }),
            "story_description": forms.Textarea(attrs={
                "class": "form-control trip-story-description-input"
            }),
            "display_order": forms.HiddenInput(),
        }


class TripItemForm(forms.ModelForm):

    # Optional title (you already use fallback logic)
    title = forms.CharField(required=False)

    # 🔴 CRITICAL FIX: prevent formset validation error
    display_order = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Keep your category ordering
        self.fields["category"].queryset = Category.objects.order_by("display_order")

        # ✅ Ensure display_order NEVER blocks validation
        self.fields["display_order"].required = False

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
            # ❌ DO NOT include display_order here anymore
            # ✅ ADD THESE
            "story_title": forms.TextInput(attrs={
                "class": "story-title form-control"
            }),
            "story_description": forms.Textarea(attrs={
                "class": "story-description form-control"
            }),
            "day_night": forms.Select(attrs={"class": "form-control mb-2"}),
            "weather": forms.Select(attrs={"class": "form-control mb-2"}),
            "travel_date": forms.DateInput(attrs={
                "class": "form-control mb-2",
                "type": "date"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        if not any(cleaned_data.values()):
            self.cleaned_data = {}
            return cleaned_data

        title = cleaned_data.get("title")
        story_title = cleaned_data.get("story_title")

        # ✅ Smart fallback: use story_title if title missing
        if not title and story_title:
            cleaned_data["title"] = story_title

        return cleaned_data


# -----------------------------
# CREATE FORMSET (with extras)
# -----------------------------
TripItemCreateFormSet = inlineformset_factory(
    Trip,
    TripItem,
    form=TripItemForm,
    fields="__all__",
    extra=5,   # Needed for tabs
    can_delete=True
)

# -----------------------------
# EDIT FORMSET (no extras)
# -----------------------------
TripItemEditFormSet = inlineformset_factory(
    Trip,
    TripItem,
    form=TripItemForm,
    fields="__all__",
    extra=0,   # Critical fix
    can_delete=True
)
