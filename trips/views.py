from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import models
from django.views import generic
from django.utils.text import slugify
from .models import Trip, TripItem
from .forms import TripForm, TripItemCreateFormSet, TripItemEditFormSet
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

            context_title=item.context_title or item.description,
            context_description=item.context_description,

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
                models.Q(
                    description="",
                    story_title="",
                    story_description="",
                    image=""
                )
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

    first_with_coords = TripItem.objects.filter(
        trip=trip,
        latitude__isnull=False,
        longitude__isnull=False
        ).exclude(
            latitude=0,
            longitude=0
        ).order_by("id").first()

    trip_info = first_with_coords if first_with_coords else TripItem(
        trip=trip,
        category=None,
        context_title=trip.title,
        context_description=trip.description,
        story_title=trip.title,
        story_description=trip.description,
        image=None,
        travel_date=None,
        weather="",
        day_night="day",
        display_order=0,
    )

    trip_info_category = Category(
        name="Trip Info",
        display_order=0
    )

    trip_info_item = TripItem(
        trip=trip,
        category=None,

        context_title=trip.title,
        context_description=trip.description,

        story_title=trip.title,
        story_description=trip.description,

        image=first_image.image if first_image else None,
        travel_date=first_image.travel_date if first_image else None,

        weather=first_image.weather if first_image and first_image.weather else "",
        day_night=first_image.day_night if first_image and first_image.day_night else "day",

        # ✅ ADD THIS FIX
        latitude=first_with_coords.latitude if first_with_coords else None,
        longitude=first_with_coords.longitude if first_with_coords else None,

        display_order=0,
    )

    trip_info = trip_info_item

    return render(
        request,
        "trips/trip_detail.html",
        {
            "itinerary": trip,
            "trip": trip,
            "trip_info": trip_info,
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

    # ✅ Always load categories first (used in both GET + POST)
    categories = Category.objects.order_by("display_order")

    # Add this:
    category_map = {cat.name.lower(): cat.id for cat in categories}

    if request.method == "POST":

        form = TripForm(request.POST, request.FILES)

        # ✅ FIX: No instance= on POST — avoids unsaved FK reference
        formset = TripItemCreateFormSet(
            request.POST,
            request.FILES,
            prefix="items"
        )

        print("------------ POST DATA ------------")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        print("------------ FORMSET ERRORS ------------")
        print(formset.errors)

        print("------------ MANAGEMENT FORM ------------")
        print(formset.management_form.errors)

        print("TOTAL_FORMS:", request.POST.get("items-TOTAL_FORMS"))
        print("INITIAL_FORMS:", request.POST.get("items-INITIAL_FORMS"))

        if form.is_valid() and formset.is_valid():

            trip = form.save(commit=False)
            trip.owner = request.user

            trip.latitude = request.POST.get("latitude") or None
            trip.longitude = request.POST.get("longitude") or None
            trip.country_code = request.POST.get("country_code") or ""

            trip.save()  # ✅ Real PK exists from this point on

            items = sorted(
                formset.save(commit=False),
                key=lambda x: x.display_order or 0
            )

            for index, item in enumerate(items):

                item.trip = trip  # ✅ Assign the saved trip with a real PK
                item.display_order = index + 1

                # ✅ Category safety fallback
                if not item.category:
                    try:
                        item.category = categories[index % len(categories)]
                    except:
                        item.category = categories.first()

                item.save()

            formset.save_m2m()

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

        # ✅ GET branch: instance=Trip() is fine — only renders empty form fields
        formset = TripItemCreateFormSet(
            instance=Trip(),
            prefix="items"
        )

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

    trip = get_object_or_404(
        Trip,
        pk=pk,
        owner=request.user
    )

    # Always load categories first
    categories = Category.objects.order_by("display_order")

    # Add this:
    category_map = {cat.name.lower(): cat.id for cat in categories}

    if request.method == "POST":

        form = TripForm(
            request.POST,
            request.FILES,
            instance=trip
        )

        formset = TripItemEditFormSet(
            request.POST,
            request.FILES,
            instance=trip,
            prefix="items"
        )

        print("------------ POST DATA ------------")
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        print("------------ FORMSET ERRORS ------------")
        print(formset.errors)

        print("------------ MANAGEMENT FORM ------------")
        print(formset.management_form.errors)

        print("TOTAL_FORMS:", request.POST.get("items-TOTAL_FORMS"))
        print("INITIAL_FORMS:", request.POST.get("items-INITIAL_FORMS"))

        if form.is_valid() and formset.is_valid():

            trip = form.save(commit=False)

            lat = request.POST.get("latitude")
            lng = request.POST.get("longitude")
            if lat:
                trip.latitude = float(lat)
            if lng:
                trip.longitude = float(lng)

            country_code = request.POST.get("country_code")
            if country_code:
                trip.country_code = country_code

            trip.save()

            items = sorted(
                formset.save(commit=False),
                key=lambda x: x.display_order or 0
            )

            for index, item in enumerate(items):
                item.trip = trip
                item.display_order = index + 1

                # Don't wipe existing coords if edit form submitted empty values
                if not item.latitude and not item.longitude:
                    existing = TripItem.objects.filter(
                        pk=item.pk
                    ).values('latitude', 'longitude').first()
                    if existing:
                        item.latitude = item.latitude or existing['latitude']
                        item.longitude = item.longitude or existing['longitude']

                # Category fallback
                if not item.category:
                    try:
                        item.category = categories[index % len(categories)]
                    except:
                        item.category = categories.first()

                item.save()

            # Handle deletions
            for obj in formset.deleted_objects:
                obj.delete()

            formset.save_m2m()

            # ✅ Sync linked itinerary if one exists
            linked_itinerary = trip.published_itineraries.first()

            if linked_itinerary:

                # Sync top-level fields
                linked_itinerary.title = trip.title
                linked_itinerary.description = trip.description
                linked_itinerary.location_name = trip.destination
                linked_itinerary.country_code = trip.country_code
                linked_itinerary.country_name = trip.country_name or trip.destination or ""
                linked_itinerary.save()

                # Wipe and resync all items
                linked_itinerary.items.all().delete()

                for item in trip.items.all().order_by("display_order"):
                    if not item.category:
                        continue
                    ItineraryItem.objects.create(
                        itinerary=linked_itinerary,
                        category=item.category,
                        context_title=item.context_title or item.description,
                        context_description=item.context_description,
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

            messages.success(
                request,
                "Trip updated successfully!"
            )

            return redirect(
                "trips:trip_detail",
                pk=trip.pk
            )

        else:
            print("FORM ERRORS:", form.errors)
            print("FORMSET ERRORS:", formset.errors)

            messages.error(
                request,
                "❌ Something went wrong. Check errors below."
            )

    else:

        form = TripForm(instance=trip)

        formset = TripItemEditFormSet(
            instance=trip,
            prefix="items"
        )

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