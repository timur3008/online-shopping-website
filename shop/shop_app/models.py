from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='Слаг')
    image = models.ImageField(upload_to='category/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название продукта')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена продукта')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    preview = models.ImageField(upload_to='article/preview/', verbose_name='Фото продукта', null=True, blank=True)
    description = models.TextField(verbose_name='Описание продукта', null=True, blank=True)

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery', verbose_name='Продукт')
    image = models.ImageField(upload_to='article/gallery', verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Картина'
        verbose_name_plural = 'Картинки'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_total_quantity(self):
        cart_items = self.items.all()
        total_quantity = sum([product.quantity for product in cart_items])
        return total_quantity

    @property
    def get_cart_total_price(self):
        cart_items = self.items.all()
        total_price = sum([product.get_total_price for product in cart_items])
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)


class ProductFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комменитарии'