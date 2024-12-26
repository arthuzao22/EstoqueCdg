from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        try:
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                
                # Verificar se o usuário está autenticado após o login
                if request.user.is_authenticated:
                    messages.success(request, "Login bem-sucedido.")
                    return redirect('home')
                else:
                    messages.error(request, "Falha ao autenticar o usuário.")
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios_login.html', {'form': form})
