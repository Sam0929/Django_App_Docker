"""
Additional integration tests for user authentication and transactions
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from transactions.models import Transaction
from decimal import Decimal


class UserAuthenticationIntegrationTestCase(TestCase):
    """Testes de integração de autenticação de usuários"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
    
    def test_complete_user_registration_and_login_flow(self):
        """Testa fluxo completo de registro e login"""
        # Registrar novo usuário
        response = self.client.post(reverse('users:login'), {
            'submit_register': 'Submit',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        
        # Verificar que usuário foi criado
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        
        # Fazer login com novo usuário
        response = self.client.post(reverse('users:login'), {
            'submit_login': 'Submit',
            'username': 'newuser',
            'password': 'ComplexPass123!',
            'remember_me': True
        })
        
        # Acessar página protegida
        response = self.client.get(reverse('users:home'))
        self.assertEqual(response.status_code, 200)


class TransactionDataConsistencyTestCase(TestCase):
    """Testes de consistência de dados de transações"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
    
    def test_user_isolation_across_multiple_transactions(self):
        """Testa isolamento de dados entre usuários"""
        # User1 cria transações
        for i in range(5):
            Transaction.objects.create(
                user=self.user1,
                name=f'User1 Transaction {i}',
                value=Decimal('100.00')
            )
        
        # User2 cria transações
        for i in range(3):
            Transaction.objects.create(
                user=self.user2,
                name=f'User2 Transaction {i}',
                value=Decimal('200.00')
            )
        
        # Verificar isolamento
        user1_transactions = Transaction.objects.filter(user=self.user1)
        user2_transactions = Transaction.objects.filter(user=self.user2)
        
        self.assertEqual(user1_transactions.count(), 5)
        self.assertEqual(user2_transactions.count(), 3)
        
        # Verificar que User1 só vê suas transações
        for trans in user1_transactions:
            self.assertEqual(trans.user, self.user1)


class CRUDOperationsFullFlowTestCase(TestCase):
    """Testes completos de CRUD com diferentes cenários"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='cruduser',
            email='crud@example.com',
            password='crudpass123'
        )
    
    def test_bulk_transaction_creation_and_retrieval(self):
        """Testa criação em lote e recuperação de transações"""
        self.client.login(username='cruduser', password='crudpass123')
        
        # Criar múltiplas transações
        transactions_data = [
            {'name': 'Transaction 1', 'value': '500.00', 'description': 'First'},
            {'name': 'Transaction 2', 'value': '-100.00', 'description': 'Second'},
            {'name': 'Transaction 3', 'value': '250.00', 'description': 'Third'},
        ]
        
        for data in transactions_data:
            self.client.post(reverse('transactions:create'), data)
        
        # Verificar todas foram criadas
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 200)
        
        # Contar transações no context
        transactions = response.context['transactions']
        self.assertEqual(len(list(transactions)), 3)


class FinancialDataIntegrityTestCase(TestCase):
    """Testes de integridade de dados financeiros"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.user = User.objects.create_user(
            username='financeuser',
            email='finance@example.com',
            password='financepass123'
        )
    
    def test_decimal_precision_integrity(self):
        """Testa integridade de precisão decimal em operações"""
        # Criar transações com valores decimais específicos
        trans1 = Transaction.objects.create(
            user=self.user,
            name='Income',
            value=Decimal('1000.50')
        )
        trans2 = Transaction.objects.create(
            user=self.user,
            name='Expense',
            value=Decimal('-250.75')
        )
        
        # Calcular totais
        income_total = Transaction.objects.filter(
            user=self.user,
            value__gt=0
        ).aggregate(total=__import__('django.db.models', fromlist=['Sum']).Sum('value'))['total']
        
        expense_total = Transaction.objects.filter(
            user=self.user,
            value__lt=0
        ).aggregate(total=__import__('django.db.models', fromlist=['Sum']).Sum('value'))['total']
        
        self.assertEqual(income_total, Decimal('1000.50'))
        self.assertEqual(expense_total, Decimal('-250.75'))
