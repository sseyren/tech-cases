from django.shortcuts import render
from django.views import generic
from django import urls

from .models import Customer
from .forms import CustomerForm, CustomerSearchForm

class CustomerListView(generic.ListView):
    model = Customer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET:
            self._search_form = CustomerSearchForm(self.request.GET)
        else:
            self._search_form = CustomerSearchForm()

        if self._search_form.is_valid():
            filter_args = {
                f"{field}__icontains": value
                for field, value in self._search_form.cleaned_data.items()
                if value and field != "page_size"
            }
            queryset = queryset.filter(**filter_args)

        return queryset

    def get_paginate_by(self, *args, **kwargs):
        if self._search_form.is_valid():
            return self._search_form.cleaned_data["page_size"]
        else:
            return 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self._search_form

        queries = self.request.GET.copy()
        if "page" in queries:
            del queries["page"]
        context["queries"] = queries

        return context

class CustomerCreateView(generic.edit.CreateView):
    model = Customer
    form_class = CustomerForm

class CustomerDetailView(generic.DetailView):
    model = Customer

class CustomerUpdateView(generic.UpdateView):
    model = Customer
    form_class = CustomerForm

class CustomerDeleteView(generic.DeleteView):
    model = Customer
    success_url = urls.reverse_lazy("list")