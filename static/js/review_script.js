document.addEventListener("DOMContentLoaded", function() {
    console.log("✅ JavaScript Loaded!");

    // Select elements
    const reviewFormContainer = document.getElementById("review-form-container");
    const reviewForm = document.getElementById("review-form");
    const commentInput = document.getElementById("comment");
    const reviewIdInput = document.getElementById("review-id");
    const submitButton = reviewForm.querySelector("button[type='submit']");
    const editButtons = document.querySelectorAll(".edit-review-btn");
    const deleteButtons = document.querySelectorAll(".delete-review-btn");

    // ✅ Ensure all form elements exist before running
    if (!reviewFormContainer || !reviewForm || !commentInput || !reviewIdInput || !submitButton) {
        console.error("❌ ERROR: Missing form elements! JavaScript will not run.");
        return;
    }

    // ✅ Automatically show the form if the user has NOT submitted any reviews
    if (!document.querySelector(".edit-review-btn")) {
        console.log("🆕 No existing review found. Showing the form.");
        reviewFormContainer.style.display = "block"; // Show form for first-time review
    } else {
        reviewFormContainer.style.display = "none"; // Hide if a review exists
    }

    // ✅ Function to show the form when editing a review
    function showReviewForm(reviewId, rating, comment) {
        console.log(`📝 Editing Review - ID: ${reviewId}, Rating: ${rating}, Comment: ${comment}`);

        reviewIdInput.value = reviewId;
        document.getElementById("rating").value = rating;
        commentInput.value = comment;
        submitButton.textContent = "Update Review";

        // ✅ Show the form
        reviewFormContainer.style.display = "block";
        commentInput.focus();
    }

    // ✅ Attach event listeners to all "Edit" buttons
    editButtons.forEach(button => {
        button.addEventListener("click", function() {
            const reviewId = this.getAttribute("data-review-id");
            const rating = this.getAttribute("data-rating");
            const comment = this.getAttribute("data-comment");

            if (!reviewId || !rating || comment === null) {
                console.error("❌ ERROR: Missing data attributes in Edit button!");
                return;
            }

            showReviewForm(reviewId, rating, comment);
        });
    });

    // ✅ Show form again after removing a review
    deleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            setTimeout(() => {
                console.log("🗑️ Review Removed! Showing form for new review...");

                // ✅ Reset form for a new review
                reviewForm.reset();
                reviewIdInput.value = "";
                submitButton.textContent = "Submit Review";
                reviewFormContainer.style.display = "block"; // Show form for new review
                commentInput.focus();

                console.log("✅ Form is ready for new review!");
            }, 500); // Delay to allow deletion to process
        });
    });

    // ✅ Hide the form after submission and clear fields
    reviewForm.addEventListener("submit", function(event) {
        console.log("📨 Review Submitted! Hiding form...");

        setTimeout(() => {
            reviewForm.reset();
            reviewIdInput.value = "";
            submitButton.textContent = "Submit Review";
            reviewFormContainer.style.display = "none";
            console.log("✅ Form Cleared and Hidden!");
        }, 300);
    });
});
