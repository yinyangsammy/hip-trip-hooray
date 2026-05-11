# itineraries/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Itinerary
from .forms import CommentForm


class ItineraryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.itinerary = Itinerary.objects.create(
            author=self.user,
            title="Rome",
            slug="rome",
            country_name="Italy",
            published=True
        )

    def test_itinerary_str(self):
        self.assertEqual(str(self.itinerary), "Rome")

    def test_itinerary_get_absolute_url(self):
        url = self.itinerary.get_absolute_url()
        self.assertIn("rome", url)
        self.assertIn("italy", url)

    def test_unpublished_itinerary_hidden_from_list(self):
        Itinerary.objects.create(
            author=self.user,
            title="Draft Trip",
            slug="draft-trip",
            published=False
        )
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("itineraries:itinerary_list"))
        titles = [i.title for i in response.context["itineraries"]]
        self.assertNotIn("Draft Trip", titles)


class CommentTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.itinerary = Itinerary.objects.create(
            author=self.user,
            title="Rome",
            slug="rome",
            country_name="Italy",
            published=True
        )

    def test_comment_form_valid(self):
        form = CommentForm(data={"body": "Great itinerary!"})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_empty(self):
        form = CommentForm(data={"body": ""})
        self.assertFalse(form.is_valid())

    def test_comment_requires_login(self):
        response = self.client.post(
            reverse(
                "itineraries:itinerary_detail",
                args=["rome", "italy"]
            ),
            {"body": "Test comment"}
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/ideas/italy/rome/"
        )
