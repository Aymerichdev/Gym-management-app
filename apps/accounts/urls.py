from django.urls import path

from apps.accounts.views import (
    AdminDashboardView,
    AdminLoginView,
    AdminLogoutView,
    AdminPasswordChangeView,
    CoachCreateView,
    MembershipPriceUpdateView,
)

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", AdminLogoutView.as_view(), name="logout"),
    path("admin-panel/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("admin-panel/coaches/new/", CoachCreateView.as_view(), name="coach-create"),
    path(
        "admin-panel/memberships/<int:pk>/price/",
        MembershipPriceUpdateView.as_view(),
        name="membership-price-update",
    ),
    path("admin-panel/password/", AdminPasswordChangeView.as_view(), name="password-change"),
]
