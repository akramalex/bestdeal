from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal


def bag_contents(request):
    """
    Context processor for shopping bag.
    Ensures VAT is **only applied** to VAT-applicable products.
    """
    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})

    vat_total = Decimal('0.00')  # ✅ Track VAT separately

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):  # ✅ Single item (no size)
            quantity = item_data
            line_total = quantity * product.price
            total += line_total
            product_count += quantity

            # ✅ Apply VAT only if product has `vat_applicable = True`
            if product.vat_applicable:
                vat_total += (line_total *
                              Decimal(settings.VAT_PERCENTAGE / 100))

            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
            })

        else:  # ✅ Handle items with sizes
            for size, quantity in item_data['items_by_size'].items():
                line_total = quantity * product.price
                total += line_total
                product_count += quantity

                # ✅ Apply VAT only if `vat_applicable = True`
                if product.vat_applicable:
                    vat_total += (line_total *
                                  Decimal(settings.VAT_PERCENTAGE / 100))

                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    # ✅ Calculate delivery cost
    if total > 0 and total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    else:
        delivery = Decimal('0.00')

    grand_total = total + vat_total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'vat': vat_total,  # ✅ Only count VAT for applicable products
        'delivery': delivery,
        'free_delivery_delta': settings.FREE_DELIVERY_THRESHOLD - total,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
