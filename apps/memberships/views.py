"""Vistas para la gestión de catálogos de membresías y precios."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.memberships.forms import MembershipForm
from apps.memberships.models import Membership


class MembershipListView(ListView):
    model = Membership
    template_name = "memberships/membership_list.html"
    context_object_name = "memberships"


class MembershipDetailView(DetailView):
    model = Membership
    template_name = "memberships/membership_detail.html"
    context_object_name = "membership"


class MembershipCreateView(CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = "memberships/membership_form.html"
    success_url = reverse_lazy("memberships:list")


class MembershipUpdateView(UpdateView):
    model = Membership
    form_class = MembershipForm
    template_name = "memberships/membership_form.html"
    success_url = reverse_lazy("memberships:list")


class MembershipDeleteView(DeleteView):
    model = Membership
    template_name = "memberships/membership_confirm_delete.html"
    context_object_name = "membership"
    success_url = reverse_lazy("memberships:list")
