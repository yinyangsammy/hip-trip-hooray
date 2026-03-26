from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Trip(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trips"
    )

    title = models.CharField(max_length=200)

    destination = models.CharField(max_length=200)

    country_name = models.CharField(max_length=200, blank=True)
    country_code = models.CharField(max_length=10, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    story_title = models.CharField(max_length=255, blank=True)
    story_description = models.TextField(blank=True)

    date = models.DateField(null=True, blank=True)
    weather = models.CharField(max_length=20, blank=True)

    description = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} — {self.owner.username}"

    def get_absolute_url(self):
        return reverse("trips:trip_detail", args=[self.pk])


class TripItem(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="items"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user_note = models.TextField(blank=True)

    image = models.ImageField(upload_to="trip_images/", blank=True, null=True)

    # NEW STORY FIELDS
    story_title = models.CharField(max_length=255, blank=True)
    story_description = models.TextField(blank=True)

    date = models.DateField(null=True, blank=True)
    weather = models.CharField(max_length=20, blank=True)

    category = models.ForeignKey(
        "itineraries.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    display_order = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title