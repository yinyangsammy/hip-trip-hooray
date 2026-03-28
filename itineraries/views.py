from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Itinerary, ItineraryItem, Category, Comment
from .forms import CommentForm, ItineraryForm, ItineraryItemForm, ItineraryItemFormSet
from trips.models import Trip, TripItem


# ----------------------------------------
# TEMPLATE ITINERARY TO CREATE TRIP
# ----------------------------------------

@login_required
def use_template(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)

    # Create new trip from itinerary
    trip = Trip.objects.create(
        title=itinerary.title,
        description=itinerary.description,
        destination=itinerary.location_name,
        owner=request.user,
    )

    # Copy itinerary items → trip items
    items = ItineraryItem.objects.filter(itinerary=itinerary)

    for item in items:
        TripItem.objects.create(
            trip=trip,
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

    messages.success(request, "Trip created from template!")
    return redirect("trips:trip_edit", pk=trip.pk)


# -----------------------------
# ITINERARY LIST
# -----------------------------
def itinerary_list(request):

    itineraries = Itinerary.objects.filter(published=True)

    return render(
        request,
        "itineraries/itinerary_list.html",
        {"itineraries": itineraries},
    )

  
# -----------------------------
# USER ITINERARY LIST
# -----------------------------
@login_required
def user_itineraries(request):

    itineraries = Itinerary.objects.filter(
        author=request.user
    ).order_by("-created_on")

    return render(
        request,
        "itineraries/user_itineraries.html",
        {
            "itineraries": itineraries,
        },
    )


# -----------------------------
# ITINERARY DETAIL
# -----------------------------
def itinerary_detail(request, slug, country=None):

    itinerary = get_object_or_404(
        Itinerary.objects.prefetch_related("items__category"),
        slug=slug,
    )

    # Allow author to view unpublished
    if not itinerary.published:
        if not request.user.is_authenticated or request.user != itinerary.author:
            return HttpResponseForbidden()

    # Correct SEO country slug
    correct_country = (
        slugify(itinerary.country_name)
        if itinerary.country_name
        else "world"
    )

    # Only redirect if country missing or incorrect
    if not country or country != correct_country:
        return redirect(
            "itineraries:itinerary_detail",
            slug=slug,
            country=correct_country
        )

    # Approved comments
    comments = itinerary.comments.filter(
        approved=True
    ).select_related("author")

    comment_form = CommentForm()

    # Categories ordered
    categories = Category.objects.order_by("display_order")

    category_items = {}

    items = itinerary.items.all()

    for category in categories:
        filtered = [
            item for item in items
            if item.category == category
        ]
        if filtered:
            category_items[category] = filtered

    # Comment submission
    if request.method == "POST":

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():

            comment = comment_form.save(commit=False)
            comment.itinerary = itinerary
            comment.author = request.user
            comment.save()

            messages.success(
                request,
                "Your comment has been submitted and is awaiting approval.",
            )

            return redirect(
                "itineraries:itinerary_detail",
                slug=slug,
                country=correct_country
            )

    return render(
        request,
        "itineraries/itinerary_detail.html",
        {
            "itinerary": itinerary,
            "category_items": category_items,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


# -----------------------------
# EDIT ITEM NOTE
# -----------------------------
@login_required
def edit_item_note(request, item_id):

    item = get_object_or_404(ItineraryItem, id=item_id)
    itinerary = item.itinerary

    # Security check
    if itinerary.author != request.user:
        return redirect(
            "itineraries:itinerary_detail",
            slug=itinerary.slug,
            country=slugify(itinerary.country_name)
        )

    if request.method == "POST":

        item.user_note = request.POST.get("user_note", "")
        item.save()

        messages.success(request, "Note updated!")

        return redirect(
            "itineraries:itinerary_detail",
            slug=itinerary.slug,
            country=slugify(itinerary.country_name)
        )

    return render(
        request,
        "itineraries/edit_item_note.html",
        {"item": item}
    )


# -----------------------------
# COMMENT EDIT
# -----------------------------
@login_required
def comment_edit(request, slug, comment_id):

    itinerary = get_object_or_404(Itinerary, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":

        comment_form = CommentForm(
            data=request.POST,
            instance=comment
        )

        if comment_form.is_valid():

            comment = comment_form.save(commit=False)
            comment.itinerary = itinerary
            comment.save()

            messages.success(request, "Comment updated!")

        else:
            messages.error(request, "Error updating comment.")

    return redirect(
        "itineraries:itinerary_detail",
        slug=slug,
        country=slugify(itinerary.country_name)
    )


# -----------------------------
# COMMENT DELETE
# -----------------------------
@login_required
def comment_delete(request, slug, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden()

    itinerary = comment.itinerary

    comment.delete()

    messages.success(request, "Your comment has been deleted.")

    return redirect(
        "itineraries:itinerary_detail",
        slug=itinerary.slug,
        country=slugify(itinerary.country_name)
    )


# -----------------------------
# EDIT ITINERARY
# -----------------------------
@login_required
def itinerary_edit(request, pk):

    itinerary = get_object_or_404(
        Itinerary,
        pk=pk,
        author=request.user
    )

    if request.method == "POST":
        form = ItineraryForm(
            request.POST,
            request.FILES,
            instance=itinerary
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Itinerary updated successfully!"
            )
            return redirect("itineraries:user_itineraries")

    else:
        form = ItineraryForm(instance=itinerary)

    return render(
        request,
        "itineraries/itinerary_form.html",
        {
            "form": form,
            "itinerary": itinerary
        },
    )


# -----------------------------
# DELETE ITINERARY
# -----------------------------
@login_required
def itinerary_delete(request, pk):

    itinerary = get_object_or_404(Itinerary, pk=pk, author=request.user)

    if request.method == "POST":
        itinerary.delete()
        messages.success(request, "Itinerary deleted!")
        return redirect("itineraries:user_itineraries")

    return redirect("itineraries:user_itineraries")


# -----------------------------
# TOGGLE PUBLISH
# -----------------------------
@login_required
def toggle_publish(request, pk):

    itinerary = get_object_or_404(Itinerary, pk=pk, author=request.user)

    itinerary.published = not itinerary.published
    itinerary.save()

    return redirect("itineraries:user_itineraries")
