# trips/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Trip, TripItem
from itineraries.models import Category


class TripModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.trip = Trip.objects.create(
            owner=self.user,
            title="Rome",
            destination="Rome, Italy"
        )

    def test_trip_str(self):
        self.assertEqual(str(self.trip), "Rome — testuser")

    def test_trip_get_absolute_url(self):
        url = self.trip.get_absolute_url()
        self.assertIn(str(self.trip.pk), url)

    def test_trip_default_not_published(self):
        self.assertFalse(self.trip.is_published)


class TripViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass123"
        )
        self.trip = Trip.objects.create(
            owner=self.user,
            title="Rome",
            destination="Rome, Italy"
        )

    def test_trip_create_requires_login(self):
        response = self.client.get(reverse("trips:trip_create"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/trips/create/"
        )

    def test_trip_detail_owner_can_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("trips:trip_detail", args=[self.trip.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_trip_detail_other_user_cannot_view(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("trips:trip_detail", args=[self.trip.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_trip_delete_owner_can_delete(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("trips:trip_delete", args=[self.trip.pk])
        )
        self.assertRedirects(response, reverse("trips:user_trips"))
        self.assertFalse(Trip.objects.filter(pk=self.trip.pk).exists())

    def test_trip_delete_other_user_cannot_delete(self):
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(
            reverse("trips:trip_delete", args=[self.trip.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Trip.objects.filter(pk=self.trip.pk).exists())


class TripItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.trip = Trip.objects.create(
            owner=self.user,
            title="Rome",
            destination="Rome, Italy"
        )
        self.category = Category.objects.create(
            name="Sights",
            display_order=1
        )

    def test_trip_item_str_with_story_title(self):
        item = TripItem.objects.create(
            trip=self.trip,
            category=self.category,
            story_title="The Colosseum"
        )
        self.assertEqual(str(item), "The Colosseum")

    def test_trip_item_str_without_story_title(self):
        item = TripItem.objects.create(
            trip=self.trip,
            category=self.category,
        )
        self.assertEqual(str(item), "Trip Stop")
