import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Category, Product, Order


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    category_slug = request.GET.get('category')
    search = request.GET.get('q', '')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if search:
        products = products.filter(name__icontains=search)

    categories = Category.objects.all()
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)

    cart_count = _cart_item_count(request)

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search': search,
        'cart_count': cart_count,
    }
    return render(request, 'shopes/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:8]
    cart_count = _cart_item_count(request)

    context = {
        'product': product,
        'related': related,
        'cart_count': cart_count,
    }
    return render(request, 'shopes/product_detail.html', context)


def cart(request):
    cart_data = _get_cart(request)
    items = cart_data.get('items', [])
    total = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
    cart_count = _cart_item_count(request)

    context = {
        'items': items,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'shopes/cart.html', context)


def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)

    cart = _get_cart(request)
    items = cart['items']

    # Check if product already in cart
    found = False
    for item in items:
        if item['product_id'] == product_id:
            new_qty = item['quantity'] + quantity
            if new_qty > product.stock:
                return JsonResponse({'error': 'Not enough stock'}, status=400)
            item['quantity'] = new_qty
            found = True
            break

    if not found:
        if quantity > product.stock:
            return JsonResponse({'error': 'Not enough stock'}, status=400)
        items.append({
            'product_id': product_id,
            'product_name': product.name,
            'price': str(product.price),
            'quantity': quantity,
            'image': product.image.url if product.image else '',
            'slug': product.slug,
        })

    _save_cart(request, cart)

    return JsonResponse({'cart_count': sum(i['quantity'] for i in items)})


def update_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    cart = _get_cart(request)
    items = cart['items']

    if quantity <= 0:
        items[:] = [i for i in items if i['product_id'] != product_id]
    else:
        for item in items:
            if item['product_id'] == product_id:
                product = get_object_or_404(Product, id=product_id)
                if quantity > product.stock:
                    return JsonResponse({'error': 'Not enough stock'}, status=400)
                item['quantity'] = quantity
                break

    _save_cart(request, cart)
    return redirect('shopes:cart')


def checkout(request):
    cart_data = _get_cart(request)
    items = cart_data.get('items', [])

    if not items:
        return redirect('shopes:product_list')

    total = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
    cart_count = _cart_item_count(request)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '')
        customer_phone = request.POST.get('customer_phone', '')
        customer_address = request.POST.get('customer_address', '')

        if not all([customer_name, customer_phone, customer_address]):
            context = {
                'items': items,
                'total': total,
                'cart_count': cart_count,
                'error': 'กรุณากรอกข้อมูลให้ครบถ้วน',
            }
            return render(request, 'shopes/checkout.html', context)

        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            items=items,
            total=total,
        )

        # Reduce stock
        for item in items:
            try:
                product = Product.objects.get(id=item['product_id'])
                product.stock -= item['quantity']
                product.save()
            except Product.DoesNotExist:
                pass

        # Clear cart
        request.session['shopes_cart'] = {'items': []}

        return redirect('shopes:order_success', order_id=order.pk)

    context = {
        'items': items,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'shopes/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shopes/order_success.html', {'order': order})


# ── Helpers ──

def _get_cart(request):
    return request.session.get('shopes_cart', {'items': []})


def _save_cart(request, cart):
    request.session['shopes_cart'] = cart
    request.session.modified = True


def _cart_item_count(request):
    cart = _get_cart(request)
    return sum(item['quantity'] for item in cart.get('items', []))