from django.urls import path

from apps.memberships.views import (
    MembershipCreateView,
    MembershipDeleteView,
    MembershipDetailView,
    MembershipListView,
    MembershipUpdateView,
)

app_name = "memberships"

urlpatterns = [
    path("", MembershipListView.as_view(), name="list"),
    path("nueva/", MembershipCreateView.as_view(), name="create"),
    path("<int:pk>/", MembershipDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", MembershipUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", MembershipDeleteView.as_view(), name="delete"),
]
