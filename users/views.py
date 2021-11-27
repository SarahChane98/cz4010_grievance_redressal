from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
import re


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('is_authority'):
                email = form.cleaned_data.get('email')
                authorized = re.search(r'ntu.edu.sg$|nus.edu.sg$|smu.edu.sg$', email)
                if authorized is None:
                    messages.error(request, f'Email {email} cannot match to any authority!')
                    return redirect('register')
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# @login_required()
# def profile(request):
#     return render(request, 'users/profile.html')

