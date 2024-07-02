from django.contrib import admin
from .models import User, Profile, EmailConfirm
from .forms import CostumeUserChangeForm, CostumUserCreationForm
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib.messages import SUCCESS
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.TabularInline):
    model = Profile

@admin.register(User)
class MyUserRegisteraion(UserAdmin):
    inlines = [ProfileInline]
    form = CostumeUserChangeForm
    add_form = CostumUserCreationForm
    model=User
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'gender')
    list_display = ['get_full_name', 'get_blue_username', 'get_yellow_email', 'profile','is_active']
    search_fields = ['first_name', 'last_name', 'email']
    list_display_links = ['get_full_name', 'get_blue_username']
    radio_fields = {'gender': admin.VERTICAL}
    list_per_page = 40
    ordering = ['first_name', 'last_name', '-username']
    actions = ('activate_users', )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number')
        }),
    )

    fieldsets = (
        (
            "اطلاعات احراض حویتی",
            {
                "fields": [('username', 'email', 'password',)]
            }
        ),
        (
            "اطلاعات شخصی",
            {
                "fields": [('first_name', 'last_name',), 'gender']
            }
        ),
        (
            "اجازه ها (مجوز ها)",
            {
                "fields": ['is_active', 'is_staff', 'is_superuser', ('groups'), ('user_permissions')]
            }
        ),
        (
            "تاریخ های مهم",
            {
                "fields": ['date_joined', 'last_login']
            }
        )
    )


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        else:
            return [ProfileInline(self.model, self.admin_site)]
        
        
    @admin.display(empty_value="بدون نام", description="نام کامل")
    def get_full_name(self, obj):
        return format_html(
            '<span style="color:red">{}</span>',
            obj.get_full_name()
            )
    
    @admin.display(description="نام کاربری")
    def get_blue_username(self, obj):
        return format_html(
            '<span style="color:blue">{}</span>',
            obj.username
        )
    
    @admin.display(description="ایمیل")
    def get_yellow_email(self, obj):
        return format_html(
            '<span style="color:#ff7b13">{}</span>',
            obj.email
        )
    
    @admin.action(description="فعال کردن یوزر های انتخابی")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext(
                "%d کاربر به فعال تغییر کرد",
                "%d کاربران به حالت فعال تغییر کردند",
                updated
            ) % updated,
            SUCCESS
        )


@admin.register(Profile)
class ProfileRegister(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'get_image', 'coin']
    list_display_links = ['phone_number']
    search_fields = ['user', 'phone_number']
    list_per_page = 40
    ordering = ['user', 'phone_number']
    fieldsets = (
        (
            "مشخصات کاربر",
            {
                "fields": [('user', 'phone_number')]
            },
        ),
        (
            "اطلاعات مالی",
            {
                "fields": ["coin"]
            },
        ),
        (
            "مشخصات دیگر",
            {
                "fields": ["image", "birth_day"]
            },
        ),
    )


@admin.register(EmailConfirm)
class EmailConfirmRegister(admin.ModelAdmin):
    list_display = ['expire', 'email', 'code']
    list_display_links = ['email']
    list_per_page = 40