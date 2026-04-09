from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.views import generic
from django.urls import reverse
from .models import Trip, TripItem
from .forms import TripForm, TripItemFormSet
from itineraries.models import Category, Itinerary, ItineraryItem
from django.utils.text import slugify


@login_required
def publish_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, owner=request.user)

    # Prevent publishing twice
    if trip.is_published:
        messages.warning(request, "This trip is already published.")
        return redirect("trips:trip_detail", pk=trip.pk)

    # Create unique slug
    base_slug = slugify(trip.title)
    slug = base_slug
    counter = 1

    while Itinerary.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    # Create itinerary
    itinerary = Itinerary.objects.create(
            author=request.user,
            title=trip.title,
            description=trip.description,
            location_name=trip.destination,
            country_name=trip.country_name or trip.destination or "",
            country_code=trip.country_code,
            slug=slug,
            original_author=request.user,
            trip=trip,
            published=True,
    )

    # Copy trip items → itinerary items
    trip_items = trip.items.all()

    for item in trip_items:
        ItineraryItem.objects.create(
            itinerary=itinerary,
            category=item.category,
            story_title=item.story_title,
            story_description=item.story_description,
            image=item.image,
            latitude=item.latitude,
            longitude=item.longitude,
            travel_date=item.travel_date,
            weather=item.weather,
            day_night=item.day_night,
            context_title=item.context_title,
            display_order=item.display_order
        )

    # Mark trip as published
    trip.is_published = True
    trip.save()

    messages.success(request, "Trip published as itinerary!")

    # Redirect to itinerary detail page (slug URL later)
    return redirect(
        "itineraries:itinerary_detail",
        slug=itinerary.slug,
        country=slugify(itinerary.country_name) if itinerary.country_name else "world"
    )


# -----------------------------
# MY TRIPS
# -----------------------------
@login_required
def user_trips(request):
    trips = Trip.objects.filter(owner=request.user)
    return render(request, "trips/user_trips.html", {"trips": trips})


# -----------------------------
# TRIP DETAIL (VIEW ONLY)
# Mirrors itinerary_detail layout
# -----------------------------
@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk, owner=request.user)

    category_order = models.Case(
        models.When(name="Sights", then=0),
        models.When(name="Flavours", then=1),
        models.When(name="Experiences", then=2),
        models.When(name="Vibes", then=3),
        models.When(name="Seasons", then=4),
        default=99,
        output_field=models.IntegerField(),
    )

    categories = Category.objects.all().order_by(category_order)

    category_items = {}
    for category in categories:
        items = TripItem.objects.filter(
            trip=trip,
            category=category
        ).order_by("display_order")
        category_items[category] = list(items)

    context = {
        "itinerary": trip,   # IMPORTANT → reuse itinerary_detail template
        "trip": trip,
        "category_items": category_items,
    }

    return render(request, "trips/trip_detail.html", context)


# -----------------------------
# TRIP LIST
# -----------------------------
class TripList(LoginRequiredMixin, generic.ListView):
    model = Trip
    template_name = "trips/trip_list.html"
    paginate_by = 6
    ordering = ["-created_on"]

    def get_queryset(self):
        return Trip.objects.filter(owner=self.request.user)


# -----------------------------
# CREATE TRIP
# -----------------------------
@login_required
def trip_create(request):

    if request.method == "POST":

        form = TripForm(request.POST, request.FILES)

        temp_trip = Trip(owner=request.user)

        formset = TripItemFormSet(
            request.POST,
            request.FILES,
            instance=temp_trip
        )

        if form.is_valid() and formset.is_valid():

            trip = form.save(commit=False)
            trip.owner = request.user
            trip.save()

            items = formset.save(commit=False)

            for item in items:

                # Skip empty JS generated stops
                if not item.title:
                    continue

                item.trip = trip
                item.save()

            messages.success(request, "✅ Trip created successfully!")
            return redirect("trips:trip_detail", pk=trip.pk)

        else:

            print("FORM ERRORS:", form.errors)
            print("FORMSET ERRORS:", formset.errors)

            messages.error(
                request,
                "❌ Something went wrong. Check errors below."
            )

    else:

        form = TripForm()
        formset = TripItemFormSet(instance=Trip())

    categories = Category.objects.order_by("display_order")

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "formset": formset,
            "categories": categories,
        },
    )


# -----------------------------
# EDIT TRIP
# -----------------------------
@login_required
def trip_edit(request, pk):
    trip = get_object_or_404(Trip, pk=pk, owner=request.user)

    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        formset = TripItemFormSet(
            request.POST,
            request.FILES,
            instance=trip,
            prefix="items"
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Trip updated successfully!")
            return redirect("trips:trip_detail", pk=trip.pk)
    else:
        form = TripForm(instance=trip)
        formset = TripItemFormSet(instance=trip, prefix="items")

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "formset": formset,
            "categories": categories,
            "trip": trip,
        },
    )


# -----------------------------
# DELETE TRIP
# -----------------------------
@login_required
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk, owner=request.user)

    if request.method == "POST":
        trip.delete()
        messages.success(request, "Trip deleted successfully!")
        return redirect("trips:user_trips")

    return render(request, "trips/trip_confirm_delete.html", {"trip": trip})