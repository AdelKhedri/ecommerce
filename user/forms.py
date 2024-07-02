from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import User, Profile
from .validators import phone_number_validator

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
