from django.urls import path

from .views import (
    AdvertisementCreateView,
    AdvertisementDetailView,
    AdvertisementListView,
    AdvertisementUpdateView,
    ResponseCreateView,
)

urlpatterns = [
    path("", AdvertisementListView.as_view(), name="advertisement_list"),
    path("<int:pk>/", AdvertisementDetailView.as_view(), name="advertisement_detail"),
    path("create/", AdvertisementCreateView.as_view(), name="advertisement_create"),
    path(
        "<int:pk>/edit/", AdvertisementUpdateView.as_view(), name="advertisement_edit"
    ),
    path("<int:pk>/response/", ResponseCreateView.as_view(), name="response_create"),
]
