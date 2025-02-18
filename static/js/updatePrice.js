document.addEventListener("DOMContentLoaded", function () {
    const quantityInput = document.querySelector(".qty_input"); // Quantity input field
    const priceElement = document.querySelector(".lead.font-weight-bold.text-primary"); // Displayed price
    const addToBagForm = document.querySelector(".form"); // The form used to add to cart

    // Extract the base price from the product details
    let basePrice = parseFloat(priceElement.textContent.replace("$", "").trim());

    // Get discount tiers dynamically from the page
    let discountTiers = [];
    document.querySelectorAll(".text-muted").forEach((element) => {
        let match = element.textContent.match(/Buy (\d+) or more for \$(\d+\.\d+)/);
        if (match) {
            discountTiers.push({
                quantity: parseInt(match[1]),
                price: parseFloat(match[2]),
            });
        }
    });

    // Function to update price dynamically
    function updatePrice() {
        let quantity = parseInt(quantityInput.value) || 1; // Get current quantity
        let unitPrice = basePrice; // Default price per unit

        // Apply discount tiers if applicable
        discountTiers.forEach((tier) => {
            if (quantity >= tier.quantity) {
                unitPrice = tier.price; // Update price per unit
            }
        });

        // Update the displayed price on the product page
        priceElement.textContent = `$${unitPrice.toFixed(2)}`;

        // Create a hidden input to send the updated price to the cart
        let priceInput = document.getElementById("updated_price");
        if (!priceInput) {
            priceInput = document.createElement("input");
            priceInput.type = "hidden";
            priceInput.name = "updated_price";
            priceInput.id = "updated_price";
            addToBagForm.appendChild(priceInput);
        }
        priceInput.value = unitPrice; // Store the new unit price in the form
    }

    // Listen for changes in quantity input
    quantityInput.addEventListener("input", updatePrice);
});
