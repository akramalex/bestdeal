document.addEventListener("DOMContentLoaded", () => {
    // ✅ Correct S3 URL
    const mediaBaseUrl = "https://best-deal0.s3.eu-north-1.amazonaws.com/media/";

    // ✅ Array of background image URLs
    const backgrounds = [
        `${mediaBaseUrl}homepage1.jpg`,
        `${mediaBaseUrl}homepage2.jpg`,
        `${mediaBaseUrl}homepage3.jpg`,
        `${mediaBaseUrl}homepage4.jpg`
    ];

    let currentBackgroundIndex = 0; // Start with the first background

    // Get the promo section element
    const promoSection = document.querySelector(".promo-section");

    // ✅ Ensure promo section exists before running the script
    if (promoSection) {
        // Function to change the background image
        const changeBackground = () => {
            currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;
            promoSection.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
            promoSection.style.backgroundSize = "cover"; // ✅ Ensures the image fills the section
            promoSection.style.backgroundPosition = "center"; // ✅ Centers the background
            promoSection.style.backgroundRepeat = "no-repeat"; // ✅ Prevents repeating the image
        };

        // Change the background every 3 seconds (3000 milliseconds)
        setInterval(changeBackground, 3000);

        // ✅ Set the initial background
        promoSection.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
        promoSection.style.backgroundSize = "cover";
        promoSection.style.backgroundPosition = "center";
        promoSection.style.backgroundRepeat = "no-repeat";
    } else {
        console.error("Promo section not found.");
    }
});
