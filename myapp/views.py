from django.shortcuts import render
import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category_of_product, Manufacturer, Element_of_cart, Cart
from .forms import CartAddProductForm, CartUpdateProductForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def get_dump(request):
    file_path = os.path.join(settings.BASE_DIR, 'dump.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    
    except FileNotFoundError:
        return Jsonresponse({"error": "File not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

def hello_world(request):
    return render(request,'myapp/index.html')

def about(request):
    return render(request, 'myapp/aboutAuthor.html')

def aboutShop(request):
    return render(request, 'myapp/aboutShop.html')
    
def load_qualifications(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    
    qualifications = [
        {
            "id": item["pk"],
            "name": item["fields"]["title"],
        }
        for item in data if item.get("model") == "data.specialty"
    ]

    return qualifications

qualifications = load_qualifications("dump.json")

def get_qualification_by_id(q_id):
    for qualification in qualifications:
        if qualification.get("id") == q_id:
            return qualification
    return None

def spec(request):

    return render(request, "myapp/spec_list.html", {"qualifications": qualifications,
        'title': 'Список квалификаций'})

def specs(request, q_id: int):
    qualification = get_qualification_by_id(q_id)
    return render(request, "myapp/spec_detail.html", {"qualification": qualification,
    'title': f"Квалификация № {q_id}" }) if qualification else HttpResponse("Квалификация не найдена")

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'myapp/login.html'
    
    def get_success_url(self):
        return reverse_lazy('product_list')

def product_list(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    manufacturer = request.GET.get('manufacturer')
    search_query = request.GET.get('search')
    
    if category:
        products = products.filter(category__id=category)
    
    if manufacturer:
        products = products.filter(manufacturer__id=manufacturer)
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    categories = Category_of_product.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
    }
    return render(request, 'myapp/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'myapp/product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = Element_of_cart.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Element_of_cart, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        form = CartUpdateProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= cart_item.product.quantity_in_stock:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                # Можно добавить сообщение об ошибке
                pass
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Element_of_cart, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = Element_of_cart.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)
    
    for item in cart_items:
        item.update_form = CartUpdateProductForm(initial={'quantity': item.quantity})
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'myapp/cart.html', context)