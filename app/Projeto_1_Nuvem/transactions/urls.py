# transactions/urls.py

from django.urls import path
from .views import (TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView)

app_name = 'transactions'

urlpatterns = [
    # R: Read/Listar 
    path('', TransactionListView.as_view(), name='list'),

    # C: Create/Criar 
    path('create/', TransactionCreateView.as_view(), name='create'),

    # U: Update/Atualizar -> Página para editar um lançamento existente (ex: /transactions/5/update/)
    path('<int:pk>/update/', TransactionUpdateView.as_view(), name='update'),

    # D: Delete/Deletar -> Página para confirmar a exclusão de um lançamento
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete'),
]