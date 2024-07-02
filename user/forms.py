from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import User, Profile
from .validators import phone_number_validator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


default_attrs = {'class': 'block w-full rounded-md border-0 py-1.5 pr-10 ring-1 ring-inset focus:ring-2 focus:ring-inset sm:text-sm sm:leading-6 bg-white'}
black_input_attrs = {'class': 'ring-1 rounded-md p-1 ring-slate-300 w-full'}
error_attrs = 'text-red-900 ring-red-300 placeholder:text-red-300 focus:ring-red-500'
birth_day_attrs = {'placeholder': '1403-05-23', 'class': 'ring-1 rounded-md p-1 ring-slate-300 w-full'}

class CostumeUserChangeForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('گروه ها', is_stacked=False),
        label = 'گروه ها'
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('اجازه ها', is_stacked=False),
        label = 'اجازه دسترسی ها'
    )


class CostumUserCreationForm(UserCreationForm):
    phone_number = forms.IntegerField(validators=[phone_number_validator], widget=forms.NumberInput(attrs=default_attrs), label="شماره تلفن")

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'password')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=150, label='ایمیل', widget=forms.EmailInput(attrs=default_attrs))
    password = forms.CharField(max_length=150, label='رمزعبور', widget=forms.PasswordInput(attrs=default_attrs))


class UserSinupForm(forms.ModelForm):
    password1 = forms.CharField(max_length=150, label="رمز عبور", widget=forms.PasswordInput(attrs=default_attrs))
    password2 = forms.CharField(max_length=150, label="تکرار رمز عبور", widget=forms.PasswordInput(attrs=default_attrs))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs=default_attrs),
            'email': forms.EmailInput(attrs=default_attrs),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError(_("پسورد ها با هم مطابظقت ندارند"))
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("نام کاربری تکراری است"))
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("ایمیل تکراری است"))
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self[field].errors:
                field_name = self.fields[field].widget.attrs
                field_name.update({'class': f'{field_name} {error_attrs}'})


class ProfileForm(forms.ModelForm):
    phone_number = forms.IntegerField(label="شماره تلفن", validators=[phone_number_validator], widget=forms.NumberInput(attrs=default_attrs))

    class Meta:
        model = Profile
        exclude = ['user', 'coin']

        widgets = {
            'image': forms.FileInput(attrs=black_input_attrs),
            'birth_day': forms.DateInput(attrs=birth_day_attrs),
            'biography': forms.Textarea(attrs=black_input_attrs),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self[field].errors:
                field_name = self.fields[field].widget.attrs
                field_name.update({'class': f'{field_name} {error_attrs}'})


class ForgetPasswordForm(forms.Form):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput(attrs=default_attrs))
    password2 = forms.CharField(max_length=150, widget=forms.PasswordInput(attrs=default_attrs))

    def clean(self):
        data = super().clean()
        if data['password'] != data['password2']:
            raise ValidationError(_('پسورد ها با هم مطابقت ندارند'))
        return data