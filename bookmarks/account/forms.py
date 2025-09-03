from django import forms 
from django.contrib.auth.models import User
from .models import Profile


"""
Данный файл нужен для того чтобы юзер сам взаимодействовал с функционалом сайта
"""


class LoginForm(forms.Form):
    """
    class auth for db
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) #vidget PasswordInpt can be use for unput type="password"


class UserRegistrationForm(forms.ModelForm): 
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', 
                               widget=forms.PasswordInput)

    class Meta: 
        model = User 
        fields = ['username', 'first_name', 'email']

    def clean_password2(self): 
        """
        Данный метод проверяет пароль1 и пароль2 на соответствие 
        """
        cd = self.cleaned_data 
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']            

    def clean_email(self): 
        #Validatsia emaila
        #она не позволяет регаться с уже существующим emailam
        data = self.cleanned_data['email']
        if User.objects.filter(email=data).exists(): 
        #здесь формируется набор QuerrySetov для сверки нет ли одинаковой электронной почты
        # exist proveraet net li poxosshei pochti yshe zareganoi
            raise forms.ValidationError('Email already in user.')
        return data 


class UserEditForm(forms.ModelForm): 
    """
    Позволяет юзерам редактировать свое имя, фамилию и адресс эл.почты (Они являются встроенными атрибутами джанго в модели User)
    """
    class Meta: 
        model = User 
        fields = ['first_name', 'last_name', 'email']
    
    def clean_email(self): 
        #sdes idet validatsia email chtobi user ne mog menat svoi bivshii email 
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists(): 
            raise forms.ValidationError(' Email already in use.')
        return data 


class ProfileEditForm(forms.ModelForm): 
    """
    Позволяет редачить данные которые сохранены в моделе Profile. Юзеры смогут редачить дату своего рождения и закачивать изображения на сайт в качестве фотоснимка профиля
    """
    class Meta: 
        model = Profile 
        fields = ['date_of_birth', 'photo']



