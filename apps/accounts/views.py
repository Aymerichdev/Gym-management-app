from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.db.models import Sum, DecimalField, Value
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.accounts.forms import CoachCreateForm
from apps.accounts.models import User
from apps.memberships.forms import MembershipPriceForm
from apps.memberships.models import Membership
from apps.payments.models import Payment


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict access to the primary admin/owner account."""

    login_url = reverse_lazy("login")

    def test_func(self):
        return bool(self.request.user and self.request.user.role == User.Roles.OWNER)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return super().handle_no_permission()
        return super().handle_no_permission()


class AdminLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if user.role != User.Roles.OWNER:
            form.add_error(None, "Solo el administrador puede iniciar sesión aquí.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin-dashboard")


class AdminDashboardView(OwnerRequiredMixin, TemplateView):
    template_name = "accounts/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_paid = (
            Payment.objects.filter(status=Payment.Status.PAID)
            .aggregate(total=Coalesce(Sum("amount"), Value(Decimal("0.00")), output_field=DecimalField()))
            .get("total")
        )
        context.update(
            {
                "total_paid": total_paid,
                "memberships": Membership.objects.select_related("client").order_by("client__first_name"),
                "coach_form": CoachCreateForm(),
            }
        )
        return context


class CoachCreateView(OwnerRequiredMixin, CreateView):
    form_class = CoachCreateForm
    template_name = "accounts/coach_form.html"
    success_url = reverse_lazy("admin-dashboard")


class MembershipPriceUpdateView(OwnerRequiredMixin, UpdateView):
    model = Membership
    form_class = MembershipPriceForm
    template_name = "accounts/membership_price_form.html"
    success_url = reverse_lazy("admin-dashboard")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = Membership.objects.select_related("client").get(pk=self.kwargs["pk"])
        return kwargs


class AdminPasswordChangeView(OwnerRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("admin-dashboard")


class AdminLogoutView(LogoutView):
    next_page = reverse_lazy("login")
