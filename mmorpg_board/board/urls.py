from django.urls import path

from .views import (
    AdvertisementCreateView,
    AdvertisementDetailView,
    AdvertisementListView,
    AdvertisementUpdateView,
    ResponseAcceptView,
    ResponseCreateView,
    ResponseDeleteView,
    ResponseRejectView,
    ResponsesListView,
)

urlpatterns = [
    path("", AdvertisementListView.as_view(), name="advertisement_list"),
    path("<int:pk>/", AdvertisementDetailView.as_view(), name="advertisement_detail"),
    path("create/", AdvertisementCreateView.as_view(), name="advertisement_create"),
    path(
        "<int:pk>/edit/", AdvertisementUpdateView.as_view(), name="advertisement_edit"
    ),
    path("<int:pk>/response/", ResponseCreateView.as_view(), name="response_create"),
    path("responses/", ResponsesListView.as_view(), name="responses_list"),
    path(
        "response/<int:pk>/accept/",
        ResponseAcceptView.as_view(),
        name="response_accept",
    ),
    path(
        "response/<int:pk>/reject/",
        ResponseRejectView.as_view(),
        name="response_reject",
    ),
    path(
        "response/<int:pk>/delete/",
        ResponseDeleteView.as_view(),
        name="response_delete",
    ),
]
