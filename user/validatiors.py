from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UsernameCharValidatior(RegexValidator):
    regex = ""
    message = _(
        "نام کاربری باید انگلیسی باشد"
        "نام کاربری میتواند شامل اعداد باشد"
        "نام کاربری نباید با اعداد شروع شود"
    )


def count_username(value):
    len_value = len(value)
    if len_value < 5:
        raise ValidationError(_("نام کاربری باید بیشتر از ۴ کاراکتر باشد"))
    return value


def phone_number(value):
    pass