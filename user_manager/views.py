from django.contrib.auth import login, logout, authenticate
from django.forms.utils import ErrorList
from django.shortcuts import redirect, render

from user_manager.forms import SignUpForm, SignInForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()
            login(request, new_user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'user_manager/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                errors = form._errors.setdefault("username", ErrorList())
                errors.append("Incorrect username or password.")
    else:
        form = SignInForm()
    return render(request, 'user_manager/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('index')
