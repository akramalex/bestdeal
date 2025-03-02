from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Wishlist
from .forms import UserProfileForm
from products.models import Product
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile with order history and wishlist. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request,
                'Update failed. Please ensure the form is valid.'
            )
    else:
        form = UserProfileForm(instance=profile)

    orders = Order.objects.filter(user_profile=profile)
    wishlist_items = Wishlist.objects.filter(user=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'wishlist': wishlist_items,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """ Display the order history of the user """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id):
    """ Add a product to the wishlist """
    product = get_object_or_404(Product, id=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    if not Wishlist.objects.filter(user=profile, product=product).exists():
        Wishlist.objects.create(user=profile, product=product)
        messages.success(request, f'Added {product.name} to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')

    return redirect(
        request.META.get('HTTP_REFERER',
                         reverse('product_detail', args=[product_id]))
    )


@login_required
def remove_from_wishlist(request, product_id):
    """ Remove a product from the wishlist """
    product = get_object_or_404(Product, id=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    wishlist_item = Wishlist.objects.filter(
        user=profile, product=product
    ).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.success(
            request,
            f'Removed {product.name} from your wishlist!'
        )
    else:
        messages.warning(request, 'This product is not in your wishlist.')

    return redirect(
        request.META.get('HTTP_REFERER', reverse('profile'))
    )
