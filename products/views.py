from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details, including rated items """

    product = get_object_or_404(Product, pk=product_id)
    
    # Fetch random rated products
    rated_products = Product.objects.filter(rating__isnull=False).order_by('?')  # Fetch 6 random rated products

    context = {
        'product': product,
        'rated_products': rated_products,
    }

    return render(request, 'products/product_detail.html', context)