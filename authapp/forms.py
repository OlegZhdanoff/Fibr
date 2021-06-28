from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from authapp.models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4 fadeIn'


class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.ClearableFileInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control bg-light'
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('article', 'about_me', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control bg-light'
