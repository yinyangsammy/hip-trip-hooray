from django.contrib import admin
from .models import Itinerary, Category, ItineraryItem, Comment


class ItineraryItemInline(admin.StackedInline):
    model = ItineraryItem
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


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ("title", "location_name", "author", "published", 
                    "created_on")
    list_filter = ("published", "created_on", "location_name")
    search_fields = ("title", "description", "location_name")
    prepopulated_fields = {"slug": ("title",)}

    inlines = [ItineraryItemInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "display_order",
    )

    list_editable = (
        "display_order",
    )

    def weather_icon(self, obj):

        icons = {
            "sun": "☀",
            "cloud": "☁",
            "rain": "🌧",
            "snow": "❄",
        }

        if obj.weather:
            return f"{icons.get(obj.weather, '')} {obj.get_weather_display()}"

        return "-"

    weather_icon.short_description = "Weather" 


@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ("context_title", "context_description", "travel_date",
                    "display_order", "story_title", "itinerary", "category")
    list_filter = ("category",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "itinerary", "approved", "created_on")
    list_filter = ("approved", "created_on")
    search_fields = ("author__username", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)