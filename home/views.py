from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    if request.user.is_authenticated:
        nome = request.user.first_name  # Pega o nome de usuário
        sobrenome = request.user.last_name  # Pega o sobrenome de usuário
        username = nome + ' ' + sobrenome
    else:
        username = None  # Caso o usuário não esteja logado

    return render(request, 'home_view.html', { 'username': username })
