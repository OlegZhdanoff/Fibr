import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import FileInput
from bootstrap_datepicker_plus import DatePickerInput

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


class CustomImageFieldWidget(FileInput):
    # template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear)s %(clear_checkbox_label)s</label><br>ddd'
    template_name = "authapp/input.html"


class UserEditForm(UserChangeForm):
    # Позволит пользователям изменять свое имя, фамилию
    # и электронную почту, хранящиеся во встроенной пользовательской модели.

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email', 'password', 'birthday')
        widgets = {
            'image': CustomImageFieldWidget,
            'birthday': DatePickerInput(format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['password'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
        for name, field in self.fields.items():
            if not name == 'image':
                if field.widget.attrs.get('readonly', False):
                    field.widget.attrs['class'] = 'form-control .bg-secondary'
                else:
                    field.widget.attrs['class'] = 'form-control'

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if datetime.date.today().year - data.year < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class UserProfileEditForm(forms.ModelForm):
    # Позволит пользователям редактировать дополнительные данные,
    # сохраняемые в пользовательской модели Profile.
    # Пользователи смогут изменить свои статьи, о себе, и пол
    # для своего профиля.
    class Meta:
        model = UserProfile
        fields = ('article', 'about_me', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
