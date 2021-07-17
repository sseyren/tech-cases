from django.shortcuts import render
from django.views import generic
from django import urls

from .models import Customer

class CustomerListView(generic.ListView):
    model = Customer
    paginate_by = 2

class CustomerCreateView(generic.edit.CreateView):
    model = Customer
    fields = ["tr_id", "first_name", "last_name", "phone", "province", "district"]

class CustomerDetailView(generic.DetailView):
    model = Customer

class CustomerUpdateView(generic.UpdateView):
    model = Customer
    fields = ["tr_id", "first_name", "last_name", "phone", "province", "district"]

class CustomerDeleteView(generic.DeleteView):
    model = Customer
    success_url = urls.reverse_lazy("list")