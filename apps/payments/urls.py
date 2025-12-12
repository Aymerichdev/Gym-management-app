from django.urls import path

from apps.payments.views import (
    PaymentCreateView,
    PaymentDeleteView,
    PaymentDetailView,
    PaymentListView,
    PaymentUpdateView,
)

app_name = "payments"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("nuevo/", PaymentCreateView.as_view(), name="create"),
    path("<int:pk>/", PaymentDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", PaymentUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", PaymentDeleteView.as_view(), name="delete"),
]
