"""
Unit tests para Transaction Views
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from transactions.models import Transaction
from decimal import Decimal


class TransactionListViewTestCase(TestCase):
    """Tests para TransactionListView"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
    
    def test_transaction_list_requires_login(self):
        """Testa se lista de transações requer login"""
        response = self.client.get(reverse('transactions:list'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
    
    def test_transaction_list_shows_only_user_transactions(self):
        """Testa se usuário só vê suas próprias transações"""
        # Criar transações para diferentes usuários
        Transaction.objects.create(
            user=self.user,
            name='User Transaction',
            value=Decimal('100.00')
        )
        Transaction.objects.create(
            user=self.other_user,
            name='Other User Transaction',
            value=Decimal('200.00')
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Transaction')
        self.assertNotContains(response, 'Other User Transaction')
    
    def test_transaction_list_ordered_by_recent(self):
        """Testa se transações são ordenadas por mais recentes"""
        trans1 = Transaction.objects.create(
            user=self.user,
            name='First',
            value=Decimal('100.00')
        )
        trans2 = Transaction.objects.create(
            user=self.user,
            name='Second',
            value=Decimal('200.00')
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions:list'))
        
        transactions = response.context['transactions']
        self.assertEqual(transactions[0].id, trans2.id)
        self.assertEqual(transactions[1].id, trans1.id)


class TransactionCreateViewTestCase(TestCase):
    """Tests para TransactionCreateView"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_transaction_create_requires_login(self):
        """Testa se criação requer login"""
        response = self.client.get(reverse('transactions:create'))
        
        self.assertEqual(response.status_code, 302)
    
    def test_transaction_create_success(self):
        """Testa criação bem-sucedida de transação"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('transactions:create'), {
            'name': 'New Transaction',
            'value': '150.00',
            'description': 'Test description'
        })
        
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.name, 'New Transaction')
        self.assertEqual(transaction.value, Decimal('150.00'))
        self.assertEqual(transaction.user, self.user)


class TransactionDeleteViewTestCase(TestCase):
    """Tests para TransactionDeleteView"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            name='To Delete',
            value=Decimal('100.00')
        )
    
    def test_user_can_delete_own_transaction(self):
        """Testa se usuário pode deletar sua própria transação"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('transactions:delete', args=[self.transaction.id])
        )
        
        self.assertEqual(Transaction.objects.count(), 0)
    
    def test_user_cannot_delete_others_transaction(self):
        """Testa se usuário não pode deletar transação de outro"""
        self.client.login(username='otheruser', password='testpass123')
        
        response = self.client.post(
            reverse('transactions:delete', args=[self.transaction.id])
        )
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Transaction.objects.count(), 1)
