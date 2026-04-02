from django.contrib import admin
from .models import Trip, TripItem


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = ("title", "destination", "owner", "created_on")

    list_filter = ("created_on", "owner")

    search_fields = ("title", "destination")


@admin.register(TripItem)
class TripItemAdmin(admin.ModelAdmin):

    list_display = ("title", "trip", "category", "created_on")

    list_filter = ("category", "created_on")

    search_fields = ("title",)