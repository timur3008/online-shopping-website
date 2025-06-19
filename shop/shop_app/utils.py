from . import models

from django.http import HttpRequest

class CartForUser:
    def __init__(self, request: HttpRequest):
        self.user = request.user
        self.request = request

    def get_cart_info(self):
        cart, created = models.Cart.objects.get_or_create(user=self.user)
        cart_items = cart.items.all()

        cart_total_price = cart.get_cart_total_price
        cart_total_quantity = cart.get_cart_total_quantity

        return {
            'cart': cart,
            'cart_products': cart_items,
            'cart_total_price': cart_total_price,
            'cart_total_quantity': cart_total_quantity
        }
    
    def add_or_delete(self, product_id: int, quantity: int = 1, action: str = None):
        cart = self.get_cart_info()['cart']
        product = models.Product.objects.get(pk=product_id)
        cart_product, created = models.CartItem.objects.get_or_create(cart=cart, product=product)

        if action == 'add' and product.amount >= quantity:
            cart_product.quantity += quantity
            product.amount -= quantity
        elif action == 'clear':
            product.amount += cart_product.quantity
            cart_product.delete()
            return
        else:
            cart_product.quantity -= quantity
            product.amount += quantity
            if cart_product.quantity <= 0:
                cart_product.delete()
                return

        cart_product.save()
        product.save()


def get_cart_data(request):
    cart = CartForUser(request)
    cart_info = cart.get_cart_info()

    return {
        'cart': cart_info['cart'],
        'cart_products': cart_info['cart_products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity']
    }