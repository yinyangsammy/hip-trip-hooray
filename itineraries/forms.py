from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.forms import inlineformset_factory
from .models import Itinerary, ItineraryItem, Category, Comment


class ItineraryForm(forms.ModelForm):

    class Meta:
        model = Itinerary
        fields = [
            "title",
            "location_name",
            "description",
            "country_name",
            "published",
        ]

        labels = {
            "title": "Itinerary title",
            "location_name": "Destination",
            "description": "Tell us about this itinerary",
            "country_name": "Country",
            "published": "Publish this itinerary",
        }

        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class ItineraryItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("display_order")

    class Meta:
        model = ItineraryItem
        fields = [
            "story_title",
            "story_description",
            "user_note",
            "category",
            "travel_date",
            "weather",
            "latitude",
            "longitude",
            "display_order",
        ]

        labels = {
            "story_title": "Stop title",
            "story_description": "Describe this place",
            "user_note": "Your personal tip",
            "category": "Type of place",
        }

        help_texts = {
            "story_description": "Tell people why this stop is worth visiting.",
            "user_note": "Optional: add your own travel tip.",
        }

        widgets = {
            "story_description": forms.Textarea(attrs={"rows": 3}),
            "user_note": forms.Textarea(attrs={"rows": 2}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "display_order": forms.HiddenInput(),
        }


ItineraryItemFormSet = inlineformset_factory(
    Itinerary,
    ItineraryItem,
    form=ItineraryItemForm,
    extra=0,
    can_delete=True
)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'id': 'id_body',   # ensures JS can target it
                'placeholder': 'Share your thoughts...',
                'rows': 3,
                'class': 'comment-textarea'
            })
        }
        labels = {
            'body': '',
        }


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.form_show_labels = False
    self.helper.layout = Layout('body')
