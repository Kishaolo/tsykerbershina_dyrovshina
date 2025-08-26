from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from .forms import LoginForm 
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
