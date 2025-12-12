from django.contrib import admin
from django.urls import include, path

from apps.memberships.views import MembershipListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("memberships/", include("apps.memberships.urls")),
    path("", MembershipListView.as_view(), name="home"),
]
