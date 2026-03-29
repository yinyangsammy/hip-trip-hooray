from django.urls import path
from . import views

app_name = "trips"

urlpatterns = [
    path("", views.user_trips, name="user_trips"),
    path("create/", views.trip_create, name="trip_create"),
    path("<int:pk>/", views.trip_detail, name="trip_detail"),
    path("<int:pk>/edit/", views.trip_edit, name="trip_edit"),
    path("<int:pk>/delete/", views.trip_delete, name="trip_delete"),
    path("<int:pk>/publish/", views.publish_trip, name="publish_trip"),
]
