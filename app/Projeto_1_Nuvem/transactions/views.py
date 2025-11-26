# transactions/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Transaction
from .forms import TransactionForm
from django.contrib import messages

# R
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions' 

    def get_queryset(self):
        
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

# C
class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def form_valid(self, form):
        
        form.instance.user = self.request.user
        messages.success(self.request, "Lançamento adicionado com sucesso!")
        return super().form_valid(form)

# U
class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def form_valid(self, form):
        messages.success(self.request, "Lançamento atualizado com sucesso!")
        return super().form_valid(form)

    def test_func(self):
        
        transaction = self.get_object()
        return self.request.user == transaction.user

# D:
class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:list')

    def test_func(self):
        
        transaction = self.get_object()
        return self.request.user == transaction.user
    
    def form_valid(self, form):
        messages.success(self.request, "Lançamento excluído com sucesso!")
        return super().form_valid(form)