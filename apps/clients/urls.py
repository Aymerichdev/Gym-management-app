from django.urls import path

from apps.clients.views import (
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    ClientListView,
    ClientUpdateView,
)

app_name = "clients"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("nuevo/", ClientCreateView.as_view(), name="create"),
    path("<int:pk>/", ClientDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", ClientUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", ClientDeleteView.as_view(), name="delete"),
]
