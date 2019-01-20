from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from . forms import SignUpForm, EditProfileForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'authenticate/home.html', {})

def users(request):
    users = User.objects.all()
    return render(request, 'authenticate/users.html', {'users':users})

def profile(request):
    return render(request, 'authenticate/profile.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'ログインしました')
            return redirect('home')
        else:
            messages.warning(request, f'ログインに失敗しました')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.warning(request, f'ログアウトしました')
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'登録に成功しました')
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'プロフィールを更新しました')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f'パスワードを変更しました')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'authenticate/change_password.html', context)
