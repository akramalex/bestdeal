from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from profiles.models import Wishlist
from .models import Product, Category, Review, update_product_rating
from .forms import ProductForm
# ---------------------- #
#  ALL PRODUCTS VIEW
# ---------------------- #
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
                if sortkey == 'category':
                    sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

            if not products.exists():
                messages.warning(request, f"No products found for '{query}'.")
                return redirect(reverse('products'))

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

# ---------------------- #
#  PRODUCT DETAIL VIEW (WITH WISHLIST)
# ---------------------- #
def product_detail(request, product_id):
    """ A view to show individual product details, including wishlist status """

    product = get_object_or_404(Product, pk=product_id)
    discount_tiers = product.discounttier_set.all()
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    user_review = None
    wishlist = []

    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        wishlist = Wishlist.objects.filter(user=request.user.userprofile).values_list('product', flat=True)

    rated_products = Product.objects.filter(
        category=product.category,
        rating__isnull=False
    ).exclude(id=product.id).order_by('?')[:20]

    context = {
        'product': product,
        'discount_tiers': discount_tiers,
        'reviews': reviews,
        'user_review': user_review,
        'rated_products': rated_products,
        'wishlist': wishlist,  # ✅ Pass wishlist data to the template
    }

    return render(request, 'products/product_detail.html', context)

# ---------------------- #
#  ADD OR UPDATE REVIEW
# ---------------------- #
@login_required
def submit_review(request, product_id):
    """ Allows users to submit or update their review for a product """

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Validate rating
        if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
            messages.error(request, "Invalid rating. Please select a rating between 1 and 5.")
            return redirect('product_detail', product_id=product.id)

        rating = int(rating)

        # ✅ Check if user has already reviewed this product
        review = Review.objects.filter(product=product, user=request.user).first()

        if review:
            # ✅ If review exists, update it instead of creating a new one
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, "Your review has been updated.")
        else:
            # ✅ If no review exists, create a new one
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment,
            )
            messages.success(request, "Thank you! Your review has been submitted.")

        # ✅ Update product rating
        update_product_rating(product)

        return redirect('product_detail', product_id=product.id)

    messages.error(request, "Invalid request.")
    return redirect('product_detail', product_id=product.id)

# ---------------------- #
#  DELETE REVIEW
# ---------------------- #
@login_required
def delete_review(request, review_id):
    """ Allows users to delete their own review and updates product rating """
    
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    product = review.product  # Get the associated product
    review.delete()  # Delete review

    # ✅ Update product rating after review deletion
    update_product_rating(product)

    messages.success(request, "Your review has been deleted.")
    return redirect('product_detail', product_id=product.id)


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

def delete_product(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))