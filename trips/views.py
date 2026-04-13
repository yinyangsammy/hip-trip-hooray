from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.views import generic
from django.utils.text import slugify
from .models import Trip, TripItem
from .forms import TripForm, TripItemFormSet
from itineraries.models import Category, Itinerary, ItineraryItem


# -----------------------------
# PUBLISH TRIP
# -----------------------------
@login_required
def publish_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk, owner=request.user)

    if trip.is_published:
        messages.warning(request, "This trip is already published.")
        return redirect("trips:trip_detail", pk=trip.pk)

    # -----------------------------
    # CREATE UNIQUE SLUG
    # -----------------------------
    base_slug = slugify(trip.title)
    slug = base_slug
    counter = 1

    while Itinerary.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    # -----------------------------
    # CREATE ITINERARY
    # -----------------------------
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

    # -----------------------------
    # COPY ITEMS → ITINERARY ITEMS
    # -----------------------------
    trip_items = trip.items.all().order_by("display_order")

    for item in trip_items:

        if not item.category:
            continue

        ItineraryItem.objects.create(
            itinerary=itinerary,
            category=item.category,

            context_title=item.context_title,
            context_description=item.context_description or item.description,

            story_title=item.story_title,
            story_description=item.story_description,

            image=item.image,

            user_note=item.user_note,

            travel_date=item.travel_date,
            day_night=item.day_night,
            weather=item.weather,

            latitude=item.latitude,
            longitude=item.longitude,

            display_order=item.display_order,
        )
        
    # -----------------------------
    # MARK AS PUBLISHED
    # -----------------------------
    trip.is_published = True
    trip.save()

    messages.success(request, "Trip published as itinerary!")

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

    category_items = []

    for category in categories:

        items = TripItem.objects.filter(
            trip=trip,
            category=category
        ).exclude(
            category__isnull=True
        ).order_by(
            "display_order", "id"
        )

    items = list(items)

    if items:
        category_items.append({
            "category": category,
            "items": items
        })

    # --------------------------------
    # Create Trip Info category (Stop 0)
    # --------------------------------

    first_image = TripItem.objects.filter(
        trip=trip
    ).exclude(
        image__isnull=True
    ).exclude(
        image=""
    ).first()

    # --------------------------------
    # Create Trip Info category (Stop 0)
    # --------------------------------

    first_image = TripItem.objects.filter(
        trip=trip
    ).exclude(
        image__isnull=True
    ).exclude(
        image=""
    ).first()

    trip_info_category = Category(
        name="Trip Info",
        display_order=0
    )

    trip_info_item = TripItem(
        trip=trip,
        category=None,

        context_title=trip.story_title or trip.title,
        context_description=trip.description,

        story_title=trip.title,
        story_description=trip.story_description or trip.description,

        image=first_image.image if first_image else None,
        travel_date=first_image.travel_date if first_image else None,

        weather=first_image.weather if first_image and first_image.weather 
        else "",
        day_night=first_image.day_night if first_image 
        and first_image.day_night else "day",

        display_order=0,
    )
 
    category_items.insert(0, {
        "category": trip_info_category,
        "items": [trip_info_item]
    })

    return render(
        request,
        "trips/trip_detail.html",
        {
            "itinerary": trip,
            "trip": trip,
            "category_items": category_items,
        }
    )


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
            instance=temp_trip,
            prefix="items"
        )

        if form.is_valid() and formset.is_valid():

            trip = form.save(commit=False)
            trip.owner = request.user
            trip.save()

            items = formset.save(commit=False)

            for index, item in enumerate(items):
                item.trip = trip
                item.display_order = index

                # 🔥 ADD THIS SAFETY NET
                if not item.category:
                    # fallback to first category OR skip
                    item.category = Category.objects.order_by("display_order").first()

                item.save()

            formset.save_m2m()

            messages.success(request, "✅ Trip created successfully!")
            return redirect("trips:trip_detail", pk=trip.pk)

        else:
            print("FORM ERRORS:", form.errors)
            print("FORMSET ERRORS:", formset.errors)

            messages.error(request, "❌ Something went wrong. Check errors below.")

    else:
        form = TripForm()

        formset = TripItemFormSet(
            instance=Trip(),
            prefix="items"
        )

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

        form = TripForm(request.POST, request.FILES, instance=trip)

        formset = TripItemFormSet(
            request.POST,
            request.FILES,
            instance=trip,
            prefix="items"
        )

        if form.is_valid() and formset.is_valid():

            form.save()

            items = formset.save(commit=False)

            for index, item in enumerate(items):
                item.trip = trip
                item.display_order = index
                item.save()

            for obj in formset.deleted_objects:
                obj.delete()

            formset.save_m2m()

            messages.success(request, "Trip updated successfully!")
            return redirect("trips:trip_detail", pk=trip.pk)

    else:
        form = TripForm(instance=trip)

        formset = TripItemFormSet(
            instance=trip,
            prefix="items"
        )

    categories = Category.objects.order_by("display_order")

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

    return render(
        request,
        "trips/trip_confirm_delete.html",
        {"trip": trip}
    )