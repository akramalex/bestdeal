document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ bag.js has loaded!");

    // ✅ Update quantity on click
    document.querySelectorAll('.update-link').forEach(button => {
        button.addEventListener('click', function (e) {
            let form = this.previousElementSibling; // Get the previous form
            if (form && form.classList.contains('update-form')) {
                form.submit();
            }
        });
    });

    // ✅ Remove item and reload on click
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default link behavior

            let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token
            let itemId = this.id.split('remove_')[1]; // Extract product ID
            let size = this.getAttribute('data-product_size'); // ✅ Matches template attribute

            let url = `/bag/remove/${itemId}/`;
            let data = new FormData();
            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('product_size', size);

            // ✅ Perform Fetch API request
            fetch(url, {
                method: 'POST',
                body: data
            })
            .then(response => {
                if (response.ok) {
                    console.log(`✅ Product ${itemId} removed successfully.`);
                    location.reload(); // Reload after success
                } else {
                    console.error(`❌ Failed to remove product ${itemId}.`);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

