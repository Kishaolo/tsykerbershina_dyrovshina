from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm 
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
# Create your views here.


def user_login(request): 
    """
    Что делает: 
    1.создается форма на аутх
    2. созвается экземпл формы
    3.проверяется на валидность form.is_valid()
    4.if valid then begin auth for help method authenticated()
    this method input  param username, password, object request
    and return object User or None 
    5.если пользыватель не был аутх то возвр ответ Invalid Login
    """
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            cd = form.cleaned_data 
            user = authenticate(request, 
                                username=cd['username'], 
                                password=cd['password'])
            if user is not None: 
                if user.is_active: 
                    login(request, user) 
                    return HttpResponse("Authenticated successfully") 
                else:
                    return HttpResponse("Disabled account")
            else: 
                return HttpResponse("Invalid login")
    else: 
        form = LoginForm()
    return render(request, 
                  'account/login.html', 
                   {'form': form}) 


@login_required #proveraet auth usera 
def dashboard(request):
    return render(request, 
                  'account/dashboard.html', 
                  {'section': 'dashboard'})


def register(request): 
    if request.method == 'POST': 
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid(): 
            #create new object Usser, but don't save that
            new_user = user_form.save(commit=False)
            #install choisis password 
            new_user.set_password(user_form.cleaned_data['password']) # method set_password хеширует пароль перед его сохранением в бд
            # для хранения паролей используется алгоритм PBKDF2SHA1, argon2, bcrypt, scrypt
            #Save object User 
            new_user.save()
            Profile.objects.create(user=new_user) # pri registratsii bydet sozdavatsa object Profile
            return render(request, 
                          'account/register_done.html', 
                          {'user_form': user_form})
    else: 
        user_form = UserRegistrationForm()
    return render(request, 
                  'account/register.html', 
                  {'user_form': user_form})


@login_required # tolko auth useri mogut ato delat (atot decorator ato pozvolaet)
def edit(request): 
    """
    Данное представление нужно чтобы пользыватели могли редактировать свои профили
    """
    if request.method == 'POST': 
        user_form = UserEditForm(instance=request.user, 
                                 data=request.POST) #xranenie dannix v modeli User(vstroennoi)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                       data=request.POST, 
                                       files=request.FILES) #xranit dannie v modeli Profile
        if user_form.is_valid() and profile_form.is_valid(): # proverka na validnost
            user_form.save()
            profile_form.save()
            #esli dannie validni to formi soxranautsa
            messages.success(request, 'Profile updated successfully')
        else: 
            messages.error(request, 'Error updating your profile')
    else: 
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 
                  'account/edit.html', 
                  {'user_form': user_form, 
                   'profile_form': profile_form})
