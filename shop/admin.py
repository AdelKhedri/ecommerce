from django.contrib import admin
from .models import Category, Product, ProductType, ProductSpecification, ProductSpecificationValue
from django.utils.translation import ngettext
from django.contrib import messages


class ProductSpecificationInline(admin.StackedInline):
    model = ProductSpecification
    verbose_name_plural = "ویژگی های محصول"


class ProductTypeRegistration(admin.ModelAdmin):
    inlines = [ProductSpecificationInline, ]


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductRegisteration(admin.ModelAdmin):
    inlines = [ProductSpecificationValueInline]
    list_display = ['name', 'is_available', 'price', 'thumbnail_image', 'quantity']
    list_filter = ["available",]
    fieldsets = [
        (
            "مشخصات کالا",
            {
                "fields": [("name", "slug", "available"), ("category" ,"product_type"), ( "price", "quantity"), "description", "image"]
            }
        )
    ]
    list_per_page = 20
    search_fields = ("name", "category", "description")
    search_help_text = "جست و جو در محصولات"

    @admin.action(description="در دسترس کردن محصولات")
    def make_available_products(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(
            request,
            ngettext(
                "%d محصول به حالت در دست رس تغییر یافت",
                "%d محصولات به حالت در دست رس تغییر یافت",
                updated
            ) % updated,
            messages.SUCCESS
        )
    
    @admin.action(description="غیر ظ دست رس کردن محصولات")
    def make_unavailable_products(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(
            request,
            ngettext(
                "%d محصول به حالت غیر قابل دست رس تغییر یافت",
                "%d محصولات به حالت غیر قابل دست رس تغییر یافت",
                updated
            ) % updated,
            messages.SUCCESS
        )
    actions = [make_available_products,make_unavailable_products]


@admin.register(ProductSpecification)
class ProductSpecificationRegistration(admin.ModelAdmin):
    list_display = ['name', 'product_type']
    search_fields = ("name", "product_type",)



@admin.register(ProductSpecificationValue)
class ProductSpecificationValueRegistration(admin.ModelAdmin):
    list_display = ["product", "specification", "value"]
    search_fields = ("specification", "value", "product",)
    list_display_links = ["specification", "value"]

@admin.register(Category)
class CategoryRegistration(admin.ModelAdmin):
    list_display = ["name", "available"]
    list_display_links = ["available"]
    search_fields = ("name", "description", "available")
    list_filter = ["available"]


@admin.register(ProductType)
class ProductTypeRegistration(admin.ModelAdmin):
    inlines = [ProductSpecificationInline,]
    list_display = ["name", "available"]
    list_display_links = ["name", "available"]
    search_fields = ("name", "available")
    list_filter = ["available"]