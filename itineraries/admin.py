from django.contrib import admin
from .models import Itinerary, Category, ItineraryItem


class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1
    fields = ("title", "category", "display_order", "image")
    ordering = ("category", "display_order")


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ("title", "location_name", "author", "published", "created_on")
    list_filter = ("published", "created_on", "location_name")
    search_fields = ("title", "description", "location_name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ItineraryItemInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
