from django.contrib import admin
from django.urls import include, path

from apps.clients.views import ClientListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("clients/", include("apps.clients.urls")),
    path("memberships/", include("apps.memberships.urls")),
    path("payments/", include("apps.payments.urls")),
    path("", ClientListView.as_view(), name="home"),
]
