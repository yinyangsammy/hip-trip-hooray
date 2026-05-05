from django.urls import path
from . import views

app_name = "itineraries"

urlpatterns = [

    # -----------------------------
    # ITINERARY LIST
    # -----------------------------
    path(
        "",
        views.itinerary_list,
        name="itinerary_list"
    ),

    # -----------------------------
    # ITINERARY USER
    # -----------------------------
    path(
        "your-itineraries/",
        views.user_itineraries,
        name="user_itineraries",
    ),

    # -----------------------------
    # PUBLISH ITINERARY
    # -----------------------------

    path("<int:pk>/use-template/",
         views.use_template,
         name="use_template"),

    # -----------------------------
    # ITINERARY CRUD
    # -----------------------------

    # -----------------------------
    # ITINERARY EDIT
    # -----------------------------
    path(
        "<int:pk>/edit/",
        views.itinerary_edit,
        name="itinerary_edit"
    ),

    # -----------------------------
    # ITINERARY DELETE
    # -----------------------------
    path(
        "<int:pk>/delete/",
        views.itinerary_delete,
        name="itinerary_delete"
    ),

    # -----------------------------
    # ITINERARY PUBLISH / UNPUBLISH
    # -----------------------------
    path(
        "<int:pk>/toggle-publish/",
        views.toggle_publish,
        name="toggle_publish"
    ),

    path(
        'search/',
        views.search_itineraries,
        name='search_itineraries'
    ),

    # -----------------------------
    # OLD URL (no country)
    # -----------------------------
    path(
        "<slug:slug>/",
        views.itinerary_detail,
        name="itinerary_detail_old"
    ),

    # -----------------------------
    # SEO URL (with country)
    # -----------------------------
    path(
        "<slug:slug>/<slug:country>/",
        views.itinerary_detail,
        name="itinerary_detail"
    ),

    # -----------------------------
    # EDIT NOTE
    # -----------------------------
    path(
        "edit-note/<int:item_id>/",
        views.edit_item_note,
        name="edit_item_note",
    ),

    # -----------------------------
    # COMMENT EDIT
    # -----------------------------
    path(
        "<slug:slug>/edit_comment/<int:comment_id>/",
        views.comment_edit,
        name="comment_edit"
    ),

    # -----------------------------
    # COMMENT DELETE
    # -----------------------------
    path(
        "<slug:slug>/delete_comment/<int:comment_id>/",
        views.comment_delete,
        name="comment_delete"
    ),
]
