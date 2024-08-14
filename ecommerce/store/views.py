from django.shortcuts import render, get_object_or_404
from .models import Category, Product
# Create your views here.

def Store(request):
    all_products = Product.objects.all()
    context = {'my_products': all_products}
    return render(request, 'store/store.html', context)


def categories(request):
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}
    # This function is added in settings.py -> context_processors so that it can be available to all the pages.
    
    
def list_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, "store/list-category.html", {"category":category, "products":products})
    
    
def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'store/product-info.html', context)