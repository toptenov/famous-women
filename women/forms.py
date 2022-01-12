from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
    """
    Форма добавления нового поста
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Вызов конструктора базового класса forms.ModelForm, чтобы отработали его ->
        # -> стандартные действия
        self.fields['cat'].empty_label = "Не выбрано"

    class Meta:
        model = Women  # Атрибут делает связь формы с моделью Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']  # Какие поля необходимо отобразить в ->
        # -> форме
        widgets = {
            'title': forms.TextInput(attrs={'class':  'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']  # Принимаем данные, прошедшие проверку стандартного валидатора
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class RegisterUserForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    # Поля username, password1, password2 определяем отдельно вне класса Meta, потому что в классе Meta не работают ->
    # -> классы стилей-css. Это деффект Django на данный момент:
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        # Виджеты в классе Meta почему-то не присваивают полям классы-css. Это, вероятно, деффект Django:
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        # }


# Форма авторизации пользователя
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


# Форма отправки обратной связи
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Вы не робот?')
