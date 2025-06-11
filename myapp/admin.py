from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Manufacturer, Product, Category_of_product, CustomUser,Cart,Element_of_cart
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Category_of_product)
admin.site.register(Cart)
admin.site.register(Element_of_cart)