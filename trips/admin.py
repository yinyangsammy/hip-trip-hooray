from django.contrib import admin
from .models import Trip, TripItem


class TripItemInline(admin.StackedInline):

    model = TripItem

    extra = 1

    fields = (
        "category",
        "context_title",
        "context_description",
        "travel_date",
        "weather",
        "day_night",
        "story_title",
        "story_description",
        "image",
        "display_order",
    )

    ordering = ("category", "display_order")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "destination",
        "owner",
        "is_published",
        "created_on",
    )

    list_filter = (
        "is_published",
        "created_on",
        "owner",
    )

    search_fields = (
        "title",
        "destination",
        "description",
    )

    inlines = [TripItemInline]


@admin.register(TripItem)
class TripItemAdmin(admin.ModelAdmin):

    list_display = (
        "story_title",
        "trip",
        "category",
        "display_order",
    )

    list_filter = (
        "category",
    )

