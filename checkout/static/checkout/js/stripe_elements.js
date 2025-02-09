// Stripe initialization
var stripe_public_key = document.getElementById('id_stripe_public_key').textContent;
var client_secret = document.getElementById('id_client_secret').textContent;

var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var card = elements.create('card'); // Styling will be handled in CSS
card.mount('#card-element');

// Handle validation errors
card.on('change', function (event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

// Form submission
var form = document.getElementById('payment-form');
form.addEventListener('submit', function (event) {
    event.preventDefault();

    stripe.confirmCardPayment(client_secret, {
        payment_method: {
            card: card,
        },
    }).then(function (result) {
        if (result.error) {
            // Show error
            var displayError = document.getElementById('card-errors');
            displayError.textContent = result.error.message;
        } else {
            // Payment succeeded
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
