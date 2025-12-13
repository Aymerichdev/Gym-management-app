"""Vistas CRUD para pagos asociados a membresías."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.payments.forms import PaymentForm
from apps.payments.models import Payment


class PaymentListView(ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"
    paginate_by = 25
    ordering = ["-created_at"]


class PaymentDetailView(DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    success_url = reverse_lazy("payments:list")

    def form_valid(self, form):
        if self.request.user.is_authenticated and not form.instance.recorded_by:
            form.instance.recorded_by = self.request.user
        return super().form_valid(form)


class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    success_url = reverse_lazy("payments:list")

    def form_valid(self, form):
        if self.request.user.is_authenticated and not form.instance.recorded_by:
            form.instance.recorded_by = self.request.user
        return super().form_valid(form)


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = "payments/payment_confirm_delete.html"
    context_object_name = "payment"
    success_url = reverse_lazy("payments:list")
