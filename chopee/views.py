from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q

def index(request):
    categories = Category.objects.all()
    
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'popular')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
    if category_id:
        products = products.filter(category_id=category_id)
        
    if sort_by == 'latest':
        products = products.order_by('-id')
    elif sort_by == 'sales':
        products = products.order_by('-sold_count')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else: # popular
        products = products.order_by('-rating')
        
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id.isdigit() else '',
        'selected_sort': sort_by,
    }
    return render(request, 'chopee/index.html', context)
