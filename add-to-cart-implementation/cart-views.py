from django.shortcuts import render,redirect
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required

def assign_product(request):
    products = Product.objects.all()
    return render(request, 'dir/products.html' , {'products' : products })

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('products')

@login_required
def view_cart(request):
    # Get the user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Get all items in the cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    
    return render(request, 'cart/view-cart.html', context)

