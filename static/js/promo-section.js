document.addEventListener("DOMContentLoaded", () => {
    // Array of background image URLs
    const backgrounds = [
        "/media/homepage1.jpg",
        "/media/homepage2.jpg",
        "/media/homepage3.jpg",
        "/media/homepage4.jpg"
    ];

    let currentBackgroundIndex = 0; // Start with the first background

    // Get the promo section element
    const promoSection = document.querySelector(".promo-section");

    // Check if the element exists to avoid errors
    if (promoSection) {
        // Add a click event listener to the promo section
        promoSection.addEventListener("click", () => {
            // Increment the index and reset to 0 if it exceeds the array length
            currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;

            // Change the background image
            promoSection.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
        });
    } else {
        console.error("Promo section not found.");
    }
});
