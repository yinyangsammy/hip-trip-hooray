from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_order = models.PositiveIntegerField(default=1)

    header_image = models.ImageField(
        upload_to="category_headers/",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class Itinerary(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="itineraries"
    )

    original_author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="original_itineraries"
    )

    trip = models.ForeignKey(
        "trips.Trip",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_itineraries"
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )

    description = models.TextField(blank=True)

    location_name = models.CharField(
        max_length=200,
        blank=True
    )

    country_name = models.CharField(max_length=100, null=True, blank=True)

    country_code = models.CharField(max_length=2, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    published = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Itineraries"
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):

        if not self.slug:

            if self.location_name:
                slug_base = f"{self.location_name}-{self.title}"
            else:
                slug_base = self.title

            self.slug = slugify(slug_base)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        country_slug = slugify(self.country_name) if self.country_name else "world"
        return reverse(
            "itineraries:itinerary_detail",
            args=[self.slug, country_slug]
        )


class ItineraryItem(models.Model):
    """
    Individual item within an itinerary, grouped by category.
    """

    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="items"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    description = models.TextField(blank=True)

    context_title = models.CharField(
        max_length=200,
        blank=True
    )

    context_description = models.TextField(blank=True)

    travel_date = models.DateField(blank=True, null=True)

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
        default="day"
    )

    story_title = models.CharField(max_length=200)

    story_description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="itinerary_items/",
        blank=True,
        null=True
    )

    user_note = models.TextField(
        blank=True,
        help_text="Optional personal notes"
    )

    display_order = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]
        unique_together = ["itinerary", "display_order"]

    def __str__(self):
        return self.story_title


class Comment(models.Model):
    """
    User comments on itineraries, subject to approval.
    """

    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="itinerary_comments"
    )

    body = models.TextField()

    approved = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment by {self.author} on {self.itinerary}"