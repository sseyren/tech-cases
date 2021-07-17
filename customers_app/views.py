from django.shortcuts import render
from django.views import generic
from django import urls

from .models import Customer
from .forms import CustomerForm

class CustomerListView(generic.ListView):
    model = Customer
    paginate_by = 2

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