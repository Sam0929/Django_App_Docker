from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2) # Usar DecimalField é a melhor prática para dinheiro
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - R$ {self.value}'

    # Propriedade para classificar facilmente como entrada ou saída
    @property
    def is_income(self):
        return self.value > 0

    @property
    def is_expense(self):
        return self.value < 0
