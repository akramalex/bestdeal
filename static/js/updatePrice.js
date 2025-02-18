document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded!");

    const quantityInput = document.querySelector(".qty_input"); // Quantity input field
    const priceElement = document.querySelector(".lead.font-weight-bold.text-primary"); // Displayed price
    const addToBagForm = document.querySelector(".form"); // Form for adding to the cart
    let incrementButton = document.querySelector(".increment-qty"); // + Button
    let decrementButton = document.querySelector(".decrement-qty"); // - Button

    if (!quantityInput || !priceElement || !incrementButton || !decrementButton) {
        console.warn("⚠️ Missing quantity input or buttons!");
        return;
    }

    console.log("✅ Elements found, script running!");

    let basePrice = parseFloat(priceElement.textContent.replace("$", "").trim());

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

    discountTiers.sort((a, b) => a.quantity - b.quantity);

    function updatePrice() {
        let quantity = parseInt(quantityInput.value) || 1;
        let unitPrice = basePrice;

        for (let i = discountTiers.length - 1; i >= 0; i--) {
            if (quantity >= discountTiers[i].quantity) {
                unitPrice = discountTiers[i].price;
                break;
            }
        }

        priceElement.textContent = `$${unitPrice.toFixed(2)}`;

        let priceInput = document.getElementById("updated_price");
        if (!priceInput) {
            priceInput = document.createElement("input");
            priceInput.type = "hidden";
            priceInput.name = "updated_price";
            priceInput.id = "updated_price";
            addToBagForm.appendChild(priceInput);
        }
        priceInput.value = unitPrice;

        // ✅ Disable the `-` button only when quantity is 1
        decrementButton.disabled = quantity <= 1;
    }

    function changeQuantity(change) {
        let currentQuantity = parseInt(quantityInput.value) || 1;
        let newQuantity = currentQuantity + change;

        if (newQuantity >= 1) {
            quantityInput.value = newQuantity;
            updatePrice();
        }
    }

    // ✅ Fix: Remove old event listeners before adding new ones
    incrementButton.replaceWith(incrementButton.cloneNode(true));
    decrementButton.replaceWith(decrementButton.cloneNode(true));

    // Re-select buttons after replacement
    incrementButton = document.querySelector(".increment-qty");
    decrementButton = document.querySelector(".decrement-qty");

    incrementButton.addEventListener("click", function (event) {
        event.preventDefault();
        changeQuantity(1);
    });

    decrementButton.addEventListener("click", function (event) {
        event.preventDefault();
        changeQuantity(-1);
    });

    quantityInput.addEventListener("input", updatePrice);

    // ✅ Ensure correct button state on page load
    updatePrice();
});
