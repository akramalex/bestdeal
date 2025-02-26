// Scroll to top when a link with class 'btt-link' is clicked
$('.btt-link').click(function(e) {
    window.scrollTo(0, 0);
});

// Update quantity on click
$('.update-link').click(function(e) {
    var form = $(this).prev('.update-form'); // Use .quantity-form class instead of ID
    form.submit();
});

// Remove item and reload on click
$('.remove-item').click(function(e) {
    var csrfToken = "{{ csrf_token }}"; // Ensure this is populated server-side
    var itemId = $(this).attr('id').split('remove_')[1];
    var size = $(this).data('product_size');
    var url = `/bag/remove/${itemId}/`;
    var data = { 'csrfmiddlewaretoken': csrfToken, 'product_size': size };

    $.post(url, data)
        .done(function() {
            location.reload();
        });
});
