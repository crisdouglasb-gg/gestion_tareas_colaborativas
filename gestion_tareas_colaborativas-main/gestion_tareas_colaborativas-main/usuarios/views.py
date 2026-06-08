# usuarios/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def mi_perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name  = request.POST.get('last_name', '')
        request.user.save()
        return redirect('mi_perfil')
    return render(request, 'usuarios/editar.html', {'usuario': request.user})
