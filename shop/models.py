from django.db import models
from django.utils.safestring import mark_safe
from .customFields import IntegerRageField
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام")
    description = models.CharField(max_length=500, blank=True, verbose_name="درباره")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="آدرس")
    available = models.BooleanField(default=True, verbose_name="دردست رس")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="child", verbose_name="دسته بندی")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
    
    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام")
    available = models.BooleanField(default=True, verbose_name="در دست رس")

    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصولات"

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(max_length=150, verbose_name="ویژگی")

    class Meta:
        verbose_name = "نام ویژگی"
        verbose_name_plural = "نام ویژگی ها"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(max_length=500, verbose_name="نام")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    description = models.TextField(max_length=3000, blank=True, verbose_name="توضیحات")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="ادرس")
    image = models.ImageField(blank=True, verbose_name="عکس")
    price = models.IntegerField(verbose_name="قیمت")
    quantity = models.IntegerField(verbose_name="تعداد موجودی")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    available = models.BooleanField(default=True, verbose_name="در دسترس")
    related_products = models.ManyToManyField("self", blank=True, verbose_name="محصولات مرتبط")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['created',]

    def get_image(self):
        return self.image.url if self.image else "/static/images/default_product_image.png" # search for 'no image'
    
    def is_available(self):
        return True if self.available and self.quantity >= 1 else False
    
    is_available.short_description = "در دسترس و موجود"
    is_available.boolean = True
    
    def thumbnail_image(self):
        if self.image:
            return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(NO Image)'
    
    thumbnail_image.short_description = "عکس محصول"

    
    def __str__(self):
        return self.name


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, related_name="specification", on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT, verbose_name="ویژگی")
    value = models.TextField(max_length=500, verbose_name="مقدار")

    class Meta:
        verbose_name = "مقدارِ ویژگی"
        verbose_name_plural = "مقدارِ ویژگی"
    
    def __str__(self):
        return self.value


class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="کد تخفیف")
    percent = IntegerRageField(verbose_name="درصد تخفیف", min_value=1, max_value=100)
    max_use = models.IntegerField(default=1, verbose_name="حداکثر تعداد استفاده")
    current_use = models.IntegerField(default=0, verbose_name="تعداد استفاده شده")
    expire_time = models.DateTimeField(verbose_name="زمان انقضا")
    available = models.BooleanField(default=True, verbose_name="در دسترس")

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
    
    def is_available(self):
        return True if self.available and self.current_use < self.max_use else False
    
    is_available.short_description = "در دسترس"
    is_available.boolean = True

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    products = models.ManyToManyField(Product, verbose_name="محصولات")
    price = models.IntegerField(verbose_name="قیمت")
    time = models.DateTimeField(auto_now_add=True, verbose_name="زمان خرید")

    def __str__(self):
        return f"{self.user.first_name}:{self.price}"