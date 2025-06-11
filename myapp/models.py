from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError


class CustomUser(AbstractUser):
	email = models.EmailField(verbose_name='Email', unique=False)
	username = models.CharField(verbose_name='Имя пользователя', max_length=150, unique=True)
	first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
	last_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
	phone_number = models.CharField(verbose_name='Телефон', max_length=15, blank=True)


class Category_of_product(models.Model):
	title = models.CharField(verbose_name='Название', max_length=100)
	description = models.TextField(verbose_name='Описание', null= True,blank=True)

	def __str__(self):
		return f'Категория: {self.title}'

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Manufacturer(models.Model):
	title = models.CharField(verbose_name='Название производителя', max_length=100)
	country = models.CharField(verbose_name='Страна производителя', max_length=100)
	description = models.TextField(verbose_name='Описание производителя', null= True,blank=True)


	def __str__(self):
			return f'Производитель: {self.title}'

	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'

class Product(models.Model):
	title = models.CharField(verbose_name='Название товара', max_length=200)
	description = models.TextField(verbose_name='Описание товара',null= True,blank=False)
	photo = models.ImageField(verbose_name='Фото товара',null= True,blank=True)
	price = models.DecimalField(verbose_name='Цена товара',decimal_places=2, max_digits=10)
	quantity_in_stock = models.PositiveIntegerField(verbose_name='Количество товаров на складе')
	category = models.ForeignKey(Category_of_product, on_delete = models.CASCADE,verbose_name='Категория товара')
	manufacturer = models.ForeignKey(Manufacturer, on_delete = models.CASCADE,verbose_name='Производитель товара')
		

	def validation(self):
		super().clean()
		if self.price <= 0:
			raise ValidationError({'price': 'Цена должна быть положительным числом'})


	def __str__(self):
		return f'Товар: {self.title}'


	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'


class Cart(models.Model):
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'Корзина пользователя: {self.user.username}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.element_of_cart_set.all())

    class Meta:
        verbose_name = 'корзину'
        verbose_name_plural = 'корзины'

	
class Element_of_cart(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
	quantity = models.PositiveIntegerField(verbose_name='Количество единиц товара в корзине')

	def __str__(self):
		return f'{self.product.title} ({self.quantity}шт.)'
	
	def get_total_price(self):
		return self.product.price * self.quantity
	
	def validation_quantity(self):
		if self.quantity <= 0 or self.quantity > self.product.quantity_in_stock:
			return "Invalid quantity"
		return "Valid quantity"
	
	class Meta:
		verbose_name = 'Элемент корзины'
		verbose_name_plural = 'Элементы корзины'