"""
Unit tests para User Model
"""
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class ProfileModelTestCase(TestCase):
    """Tests para o modelo Profile"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation_on_user_creation(self):
        """Testa se Profile é criado automaticamente ao criar User"""
        profile = Profile.objects.filter(user=self.user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)
    
    def test_profile_string_representation(self):
        """Testa representação em string do Profile"""
        profile = self.user.profile
        self.assertEqual(str(profile), 'testuser')
    
    def test_profile_bio_field(self):
        """Testa campo bio do Profile"""
        profile = self.user.profile
        profile.bio = 'Test bio'
        profile.save()
        
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'Test bio')
    
    def test_profile_default_avatar(self):
        """Testa avatar padrão do Profile"""
        profile = self.user.profile
        self.assertEqual(profile.avatar.name, 'default.jpg')


class UserModelTestCase(TestCase):
    """Tests para o modelo User"""
    
    def test_user_creation(self):
        """Testa criação básica de usuário"""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_has_associated_profile(self):
        """Testa se cada usuário tem um Profile associado"""
        user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='testpass123'
        )
        
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
    
    def test_user_with_transactions_relation(self):
        """Testa relação de usuário com transações"""
        user = User.objects.create_user(
            username='transuser',
            email='trans@example.com',
            password='testpass123'
        )
        
        # Verificar que a relação 'transactions' está disponível
        self.assertTrue(hasattr(user, 'transactions'))
