from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from . import validators


def codeGenerator():
    return uuid4().hex[:20]

class Profile(models.Model):
    coin = models.IntegerField(default=0, blank=True, verbose_name="موجودی")
    image = models.ImageField(upload_to="images/profile/", blank=True, verbose_name="عکس")
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name="کاربر")
    birth_day = models.DateField(blank=True, null=True, verbose_name="تاریخ تولد")
    phone_number = models.BigIntegerField(unique=True, verbose_name='شماره تلفن')
    biography = models.CharField(max_length=500, blank=True, default='من به فروشگاه پیوستم!', verbose_name="درباره")
    
    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
    

    def get_image(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return "no image"
    def __str__(self):
        return self.user.__str__()


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValidationError("کاربر باید دارای نام کاربری باشد")
        if not email:
            raise ValidationError("کاربر باید دارای ایمیل باشد")
        if not password:
            raise ValidationError("کاربر باید دارای پسورد باشد")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    class GenderType(models.TextChoices):
        men = 'M', 'مرد'
        women = 'W', 'زن'
    
    username = models.CharField(max_length=150, unique=True, verbose_name="یوزرنیم",
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            "unique": _("A user with that username already exists.")
        },
        validators=[validators.username_validator]) #validatiors.UsernameCharValidatior(), 
    gender = models.CharField(blank=True, choices=GenderType.choices, max_length=1, verbose_name="جنسیت")
    email = models.EmailField(max_length=255, unique=True, error_messages={'unique': 'کاربر با این ایمیل وجود دارد'}, verbose_name="ایمیل")
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def get_full_name(self):
        return super().get_full_name()
    get_full_name.short_description = 'نام کامل'
    

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username


class EmailConfirm(models.Model):
    class OtpType(models.TextChoices):
        forget_password = 'F', 'فراموشی پسورد'
        acctive_account = "S", 'تکمیل ثبت نام'
    code = models.CharField(default=codeGenerator, max_length=20, verbose_name="کد تایید ایمیل")
    expire = models.DateTimeField(verbose_name="زمان انقضا")
    email = models.EmailField(verbose_name='ایمیل')
    otp_type = models.CharField(choices=OtpType.choices, default=OtpType.acctive_account, max_length=1 , verbose_name="نوع Otp")


    class Meta:
        verbose_name = 'تاییدیه ایمیل'
        verbose_name_plural = 'تاییدیه های ایمیل ها'
    

    def __str__(self):
        return str(self.email)