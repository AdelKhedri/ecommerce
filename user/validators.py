from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from string import ascii_letters
my_chars = ascii_letters + '1234567890'

def username_validator(value):
    len_value = len(value)
    if len_value < 5:
        raise ValidationError(_("نام کاربری باید بیشتر از ۴ کاراکتر باشد"))
    for i in value:
        if i not in my_chars:
            raise ValidationError(_("نام کاربری باید انگلیسی و یا حاوی عدد باشد"))
    if value.isnumeric():
        raise ValidationError(_("نام کاربری نمیتواند فقط عدد باشد"))
    return value


def clean_password(value):
    if value.isnumeric():
        raise ValidationError(_("پسورد نباید فقط عدد باشد"))
    if value.isalpha():
        raise ValidationError(_("پسورد نباید فقط متن باشد"))
    if len(value)< 7:
        raise ValidationError(_("پسورد باید بیشتر از 7 حرف باشد"))
    return value


def phone_number_validator(value):
    str_value = str(value)
    if len(str_value) != 10:
        raise ValidationError(_("شماره تلفن باید 10 رقم باشه"))
    elif str_value[0] != '9':
        raise ValidationError(_("شماره تلفن باید با 9 شروع شود"))
    return value