from django.contrib import admin
from django.urls import include, path

from apps.clients.views import ClientListView
from apps.memberships.views import MembershipListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clients/", include("apps.clients.urls")),
    path("memberships/", include("apps.memberships.urls")),
    path("", ClientListView.as_view(), name="home"),
]
