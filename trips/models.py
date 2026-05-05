from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from itineraries.models import Category


class Trip(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trips"
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    destination = models.CharField(
        max_length=200
    )

    country_name = models.CharField(
        max_length=200,
        blank=True
    )

    country_code = models.CharField(
        max_length=10,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    story_title = models.CharField(
        max_length=255,
        blank=True
    )

    story_description = models.TextField(
        blank=True
    )

    is_published = models.BooleanField(
        default=False
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} — {self.owner.username}"

    def get_absolute_url(self):
        return reverse(
            "trips:trip_detail",
            args=[self.pk]
        )


class TripItem(models.Model):
    """
    Individual stop within a Trip.
    Mirrors ItineraryItem structure for seamless publishing.
    """

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="items"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    context_title = models.CharField(
        max_length=200,
        blank=True
    )

    context_description = models.TextField(
        blank=True
    )

    travel_date = models.DateField(
        null=True,
        blank=True
    )

    DAY_NIGHT_CHOICES = [
        ("sunrise", "Sunrise"),
        ("day", "Day"),
        ("sunset", "Sunset"),
        ("night", "Night"),
    ]

    WEATHER_CHOICES = [
        ("sun", "Sunny"),
        ("cloud", "Cloudy"),
        ("rain", "Rainy"),
        ("snow", "Snowy"),
        ("wind", "Windy"),
        ("storm", "Stormy"),
    ]

    weather = models.CharField(
        max_length=10,
        choices=WEATHER_CHOICES,
        blank=True
    )

    day_night = models.CharField(
        max_length=10,
        choices=DAY_NIGHT_CHOICES,
        default="day",
        blank=True
    )

    story_title = models.CharField(
        max_length=200,
        blank=True
    )

    story_description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="trip_items/",
        blank=True,
        null=True
    )

    user_note = models.TextField(
        blank=True,
        help_text="Optional personal notes"
    )

    is_featured = models.BooleanField(
        default=False
    )

    display_order = models.PositiveIntegerField(
        default=0,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["display_order"]
        unique_together = ["trip", "display_order"]

    def __str__(self):
        return self.story_title or "Trip Stop"