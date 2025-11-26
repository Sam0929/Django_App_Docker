from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, CustomPasswordChangeForm
from transactions.models import Transaction 
from django.db.models import Sum
from decimal import Decimal

@login_required
def home(request):

    transactions = Transaction.objects.filter(user=request.user)
   
    positive_total_dict = transactions.filter(value__gt=0).aggregate(total=Sum('value'))
    positiveTotal = positive_total_dict['total'] or Decimal('0.00')

    negative_total_dict = transactions.filter(value__lt=0).aggregate(total=Sum('value'))
    negativeTotal = negative_total_dict['total'] or Decimal('0.00')

    balance = positiveTotal + negativeTotal

    total_flow = positiveTotal + abs(negativeTotal) 
    
    if total_flow > 0:
        incomePercentage = int((positiveTotal / total_flow) * 100)
        expensePercentage = int((abs(negativeTotal) / total_flow) * 100)
    else:
        incomePercentage = 0
        expensePercentage = 0

   
    recent_transactions = transactions.order_by('-created_at')[:10]
 
    stocks = [
        {'symbol': 'PETR4', 'price': 38.50, 'changesPercentage': 1.5},       #SIMULAÇÃO, NECESSARIO API
        {'symbol': 'MGLU3', 'price': 12.70, 'changesPercentage': -0.8},
        {'symbol': 'VALE3', 'price': 65.20, 'changesPercentage': 2.1},
    ]

    
    context = {
        'balance': balance,
        'positiveTotal': positiveTotal,
        'negativeTotal': abs(negativeTotal), 
        'incomePercentage': incomePercentage,
        'expensePercentage': expensePercentage,
        'data_transactions': recent_transactions, 
        'stocks': stocks,
     
    }

    return render(request, 'users/home.html', context)

class LoginAndRegisterView(View):

    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
    
        if request.user.is_authenticated:
         
            return redirect('users:home')
      
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        register_form = RegisterForm()
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        login_form = LoginForm()
        register_form = RegisterForm()
        active_form = 'login' 

        if 'submit_login' in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)

                remember_me = login_form.cleaned_data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True

                return redirect('users:home')
         
        elif 'submit_register' in request.POST:
            active_form = 'register'
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user) 
                return redirect('users:login')
            
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'active_form': active_form, 
        }
        return render(request, self.template_name, context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users:home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = CustomPasswordChangeForm 
    success_message = "Você trocou sua senha com sucesso!"
    success_url = reverse_lazy('users:home')

def logout_view(request):
   
    logout(request)
    messages.info(request, "Você foi desconectado com sucesso.")
    return redirect('users:login') 


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect(to='users:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
