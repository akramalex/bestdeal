from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    current_sorting = f'{sort}_{direction}'


    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details, including rated items """

    # Fetch the product by ID
    product = get_object_or_404(Product, pk=product_id)

    # Fetch related discount tiers
    discount_tiers = product.discounttier_set.all()  # Fetch all DiscountTier entries related to the product

    # Fetch random rated products (example: 6 random rated products)
    rated_products = Product.objects.filter(
        category=product.category,  # Match the category
        rating__isnull=False       # Ensure they have a rating
    ).exclude(id=product.id).order_by('?')[:20]  # Exclude the current product and limit results
    # Add all relevant data to the context
    context = {
        'product': product,
        'discount_tiers': discount_tiers,  # Pass discount tiers to the template
        'rated_products': rated_products,
    }

    return render(request, 'products/product_detail.html', context)