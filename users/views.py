import re

from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto import Random
from Crypto.Cipher import AES
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            authenticated = re.search(r'ntu.edu.sg$|nus.edu.sg$|smu.edu.sg$', email)
            if authenticated is None:
                messages.error(request, f'Email {email} cannot match to any organization!')
                return redirect('register')
            
            random_generator = Random.new().read
            key = RSA.generate(1024, random_generator)  # generate pub and private key
            user = form.save()
            user.pub_key = key.publickey().exportKey()
            padded_key = pad(bytes(form.cleaned_data.get('password1'), 'utf-8'), 16)
            cipher = AES.new(padded_key, AES.MODE_EAX)
            user.nonce = cipher.nonce
            user.pri_key = cipher.encrypt(key.exportKey())
            print(AES.new(padded_key, AES.MODE_EAX, user.nonce).decrypt(user.pri_key).decode("utf-8"))
            user.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# @login_required()
# def profile(request):
#     return render(request, 'users/profile.html')

