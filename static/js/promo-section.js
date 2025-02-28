document.addEventListener("DOMContentLoaded", () => {
    const mediaBaseUrl = "https://best-deal0.s3.eu-north-1.amazonaws.com/media/";

    const backgrounds = [
        `${mediaBaseUrl}homepage1.jpg`,
        `${mediaBaseUrl}homepage2.jpg`,
        `${mediaBaseUrl}homepage3.jpg`,
        `${mediaBaseUrl}homepage4.jpg`
    ];

    let currentBackgroundIndex = 0;
    const promoSection = document.querySelector(".promo-section");

    if (promoSection) {
        const changeBackground = () => {
            currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;
            promoSection.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
            promoSection.style.backgroundSize = "cover";
            promoSection.style.backgroundPosition = "center 0%"; // ✅ Moves image down
            promoSection.style.backgroundRepeat = "no-repeat";
        };

        setInterval(changeBackground, 5000);

        // ✅ Set the initial background with correct positioning
        promoSection.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
        promoSection.style.backgroundSize = "cover";
        promoSection.style.backgroundPosition = "center 0%"; // ✅ Moves image down
        promoSection.style.backgroundRepeat = "no-repeat";
    } else {
        console.error("Promo section not found.");
    }
});