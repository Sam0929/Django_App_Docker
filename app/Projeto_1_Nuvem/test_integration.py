"""
Integration tests para o sistema de Transações
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from transactions.models import Transaction
from users.models import Profile
from decimal import Decimal


class TransactionIntegrationTestCase(TestCase):
    """Testes de integração para o fluxo completo de transações"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='integrationuser',
            email='integration@example.com',
            password='integrationpass123'
        )
    
    def test_full_transaction_crud_workflow(self):
        """Testa ciclo completo de CRUD de transações"""
        self.client.login(username='integrationuser', password='integrationpass123')
        
        # CREATE
        response = self.client.post(reverse('transactions:create'), {
            'name': 'Integration Test Transaction',
            'value': '500.00',
            'description': 'Test transaction for integration'
        })
        
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        
        # READ
        response = self.client.get(reverse('transactions:list'))
        self.assertContains(response, 'Integration Test Transaction')
        
        # UPDATE
        response = self.client.post(
            reverse('transactions:update', args=[transaction.id]),
            {
                'name': 'Updated Transaction',
                'value': '600.00',
                'description': 'Updated description'
            }
        )
        
        transaction.refresh_from_db()
        self.assertEqual(transaction.name, 'Updated Transaction')
        self.assertEqual(transaction.value, Decimal('600.00'))
    
    def test_user_authentication_and_transaction_access(self):
        """Testa autenticação de usuário e acesso a transações"""
        # Usuário não autenticado não consegue acessar
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 302)
        
        # Após login, consegue acessar
        self.client.login(username='integrationuser', password='integrationpass123')
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_financial_summary_calculation(self):
        """Testa cálculo de resumo financeiro com múltiplas transações"""
        # Criar transações de entrada e saída
        Transaction.objects.create(
            user=self.user,
            name='Salary',
            value=Decimal('5000.00')
        )
        Transaction.objects.create(
            user=self.user,
            name='Rent',
            value=Decimal('-1200.00')
        )
        Transaction.objects.create(
            user=self.user,
            name='Groceries',
            value=Decimal('-150.00')
        )
        
        # Verificar se todas as transações foram criadas
        user_transactions = Transaction.objects.filter(user=self.user)
        self.assertEqual(user_transactions.count(), 3)
        
        # Calcular totais
        income_total = sum(t.value for t in user_transactions if t.is_income)
        expense_total = sum(t.value for t in user_transactions if t.is_expense)
        
        self.assertEqual(income_total, Decimal('5000.00'))
        self.assertEqual(expense_total, Decimal('-1350.00'))
    
    def test_user_profile_integration_with_transactions(self):
        """Testa integração de perfil de usuário com transações"""
        # Verificar que profile foi criado
        self.assertTrue(hasattr(self.user, 'profile'))
        
        # Adicionar bio ao profile
        self.user.profile.bio = 'Test user with transactions'
        self.user.profile.save()
        
        # Criar transação
        Transaction.objects.create(
            user=self.user,
            name='Integration Test',
            value=Decimal('100.00')
        )
        
        # Verificar que tudo funciona junto
        user = User.objects.get(username='integrationuser')
        self.assertEqual(user.profile.bio, 'Test user with transactions')
        self.assertEqual(user.transactions.count(), 1)
    
    def test_transaction_ordering_and_filtering(self):
        """Testa ordenação e filtragem de transações"""
        trans1 = Transaction.objects.create(
            user=self.user,
            name='Income 1',
            value=Decimal('1000.00')
        )
        trans2 = Transaction.objects.create(
            user=self.user,
            name='Expense 1',
            value=Decimal('-200.00')
        )
        trans3 = Transaction.objects.create(
            user=self.user,
            name='Income 2',
            value=Decimal('2000.00')
        )
        
        # Testar filtragem por valor positivo (income)
        incomes = Transaction.objects.filter(user=self.user, value__gt=0)
        self.assertEqual(incomes.count(), 2)
        
        # Testar filtragem por valor negativo (expense)
        expenses = Transaction.objects.filter(user=self.user, value__lt=0)
        self.assertEqual(expenses.count(), 1)
        
        # Testar ordenação
        ordered = Transaction.objects.filter(user=self.user).order_by('-created_at')
        self.assertEqual(ordered[0].id, trans3.id)
