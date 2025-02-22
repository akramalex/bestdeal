document.addEventListener("DOMContentLoaded", () => {
    // ✅ Correct S3 URL for media files
    const mediaBaseUrl = "https://best-deal0.s3.eu-north-1.amazonaws.com/media/";

    // ✅ Array of background image URLs with cache-busting
    const backgrounds = [
        `${mediaBaseUrl}homepage1.jpg?v=${new Date().getTime()}`,
        `${mediaBaseUrl}homepage2.jpg?v=${new Date().getTime()}`,
        `${mediaBaseUrl}homepage3.jpg?v=${new Date().getTime()}`,
        `${mediaBaseUrl}homepage4.jpg?v=${new Date().getTime()}`
    ];

    let currentBackgroundIndex = 0;
    const promoSection = document.querySelector(".promo-section");

    // ✅ Ensure promo section exists before running the script
    if (promoSection) {
        const changeBackground = () => {
            // ✅ Update the background image
            currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;
            promoSection.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
            promoSection.style.backgroundSize = "cover";
            promoSection.style.backgroundPosition = "center 20%"; // ✅ Moves image down slightly
            promoSection.style.backgroundRepeat = "no-repeat";

            // ✅ Debugging: Log the new image URL in the console
            console.log(`Background changed to: ${backgrounds[currentBackgroundIndex]}`);
        };

        // ✅ Apply the first background immediately
        changeBackground();

        // ✅ Automatically change background every 3 seconds
        setInterval(changeBackground, 3000);
    } else {
        console.error("Promo section not found.");
    }
});
