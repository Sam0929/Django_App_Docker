"""
Unit tests para User Views
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile


class LoginAndRegisterViewTestCase(TestCase):
    """Tests para LoginAndRegisterView"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
    
    def test_login_view_get_request(self):
        """Testa carregamento da página de login"""
        response = self.client.get(reverse('users:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('login_form', response.context)
        self.assertIn('register_form', response.context)
    
    def test_login_success(self):
        """Testa login bem-sucedido"""
        response = self.client.post(reverse('users:login'), {
            'submit_login': 'Submit',
            'username': 'existinguser',
            'password': 'testpass123',
            'remember_me': True
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_register_success(self):
        """Testa registro bem-sucedido"""
        response = self.client.post(reverse('users:login'), {
            'submit_register': 'Submit',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123!',
            'password2': 'complexpass123!'
        }, follow=True)
        
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
    
    def test_authenticated_user_redirected_from_login(self):
        """Testa se usuário autenticado é redirecionado da página de login"""
        self.client.login(username='existinguser', password='testpass123')
        response = self.client.get(reverse('users:login'))
        
        self.assertEqual(response.status_code, 302)


class LogoutViewTestCase(TestCase):
    """Tests para logout"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='logoutuser',
            email='logout@example.com',
            password='testpass123'
        )
    
    def test_logout_success(self):
        """Testa logout bem-sucedido"""
        self.client.login(username='logoutuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class ProfileViewTestCase(TestCase):
    """Tests para profile view"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='testpass123'
        )
    
    def test_profile_view_requires_login(self):
        """Testa se profile requer login"""
        response = self.client.get(reverse('users:profile'))
        
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view_get_request(self):
        """Testa carregamento da página de perfil"""
        self.client.login(username='profileuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)
    
    def test_profile_update(self):
        """Testa atualização de perfil"""
        self.client.login(username='profileuser', password='testpass123')
        
        response = self.client.post(reverse('users:profile'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'newemail@example.com',
            'bio': 'Updated bio'
        })
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.email, 'newemail@example.com')


class HomeViewTestCase(TestCase):
    """Tests para home view"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='homeuser',
            email='home@example.com',
            password='testpass123'
        )
    
    def test_home_view_requires_login(self):
        """Testa se home requer login"""
        response = self.client.get(reverse('users:home'))
        
        self.assertEqual(response.status_code, 302)
    
    def test_home_view_loads_successfully(self):
        """Testa carregamento da página home"""
        self.client.login(username='homeuser', password='testpass123')
        response = self.client.get(reverse('users:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('balance', response.context)
        self.assertIn('positiveTotal', response.context)
        self.assertIn('negativeTotal', response.context)
