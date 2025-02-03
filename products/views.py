from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)


    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details, including rated items """

    # Fetch the product by ID
    product = get_object_or_404(Product, pk=product_id)

    # Fetch related discount tiers
    discount_tiers = product.discounttier_set.all()  # Fetch all DiscountTier entries related to the product

    # Fetch random rated products (example: 6 random rated products)
    rated_products = Product.objects.filter(rating__isnull=False).order_by('?')[:20]

    # Add all relevant data to the context
    context = {
        'product': product,
        'discount_tiers': discount_tiers,  # Pass discount tiers to the template
        'rated_products': rated_products,
    }

    return render(request, 'products/product_detail.html', context)