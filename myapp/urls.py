from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('', hello_world, name = 'home' ),
    path('about/', about, name='about'),
    path('aboutShop/', aboutShop, name='aboutShop'),
    path('spec/', spec, name='dump-list'),
    path("spec/<int:q_id>", specs, name="spec_detail"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('catalog/', product_list, name='product_list'),
    path('catalog/<int:pk>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

