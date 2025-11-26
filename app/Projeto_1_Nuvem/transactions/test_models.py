"""
Unit tests para Transaction Model
"""
from django.test import TestCase
from django.contrib.auth.models import User
from transactions.models import Transaction
from decimal import Decimal


class TransactionModelTestCase(TestCase):
    """Tests para o modelo Transaction"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_transaction_creation(self):
        """Testa criação básica de uma transação"""
        transaction = Transaction.objects.create(
            user=self.user,
            name='Test Transaction',
            value=Decimal('100.00'),
            description='Test description'
        )
        
        self.assertEqual(transaction.name, 'Test Transaction')
        self.assertEqual(transaction.value, Decimal('100.00'))
        self.assertEqual(transaction.user, self.user)
    
    def test_transaction_string_representation(self):
        """Testa representação em string da transação"""
        transaction = Transaction.objects.create(
            user=self.user,
            name='Salary',
            value=Decimal('5000.00')
        )
        
        expected_str = 'Salary - R$ 5000.00'
        self.assertEqual(str(transaction), expected_str)
    
    def test_transaction_is_income_property(self):
        """Testa propriedade is_income com valor positivo"""
        income = Transaction.objects.create(
            user=self.user,
            name='Income',
            value=Decimal('100.00')
        )
        
        self.assertTrue(income.is_income)
        self.assertFalse(income.is_expense)
    
    def test_transaction_is_expense_property(self):
        """Testa propriedade is_expense com valor negativo"""
        expense = Transaction.objects.create(
            user=self.user,
            name='Expense',
            value=Decimal('-50.00')
        )
        
        self.assertTrue(expense.is_expense)
        self.assertFalse(expense.is_income)
    
    def test_transaction_zero_value_not_income_not_expense(self):
        """Testa transação com valor zero"""
        zero_transaction = Transaction.objects.create(
            user=self.user,
            name='Zero Transaction',
            value=Decimal('0.00')
        )
        
        self.assertFalse(zero_transaction.is_income)
        self.assertFalse(zero_transaction.is_expense)
    
    def test_transaction_decimal_precision(self):
        """Testa precisão decimal para valores monetários"""
        transaction = Transaction.objects.create(
            user=self.user,
            name='Precise Value',
            value=Decimal('99.99')
        )
        
        self.assertEqual(transaction.value, Decimal('99.99'))
    
    def test_transaction_auto_created_timestamp(self):
        """Testa se created_at é preenchido automaticamente"""
        transaction = Transaction.objects.create(
            user=self.user,
            name='Timestamped Transaction',
            value=Decimal('50.00')
        )
        
        self.assertIsNotNone(transaction.created_at)
    
    def test_transaction_cascading_delete(self):
        """Testa se transações são deletadas ao deletar o usuário"""
        transaction = Transaction.objects.create(
            user=self.user,
            name='To Delete',
            value=Decimal('100.00')
        )
        
        transaction_id = transaction.id
        self.user.delete()
        
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=transaction_id)
    
    def test_multiple_transactions_for_same_user(self):
        """Testa múltiplas transações do mesmo usuário"""
        Transaction.objects.create(
            user=self.user,
            name='Income',
            value=Decimal('5000.00')
        )
        Transaction.objects.create(
            user=self.user,
            name='Expense',
            value=Decimal('-100.00')
        )
        
        user_transactions = Transaction.objects.filter(user=self.user)
        self.assertEqual(user_transactions.count(), 2)
