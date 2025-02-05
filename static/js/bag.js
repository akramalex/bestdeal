document.addEventListener("DOMContentLoaded", function () {
    // Update quantity on click
    document.querySelectorAll('.update-link').forEach(button => {
        button.addEventListener('click', function (e) {
            let form = this.previousElementSibling; // Get the previous form
            if (form && form.classList.contains('update-form')) {
                form.submit();
            }
        });
    });

    // Remove item and reload on click
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', function (e) {
            let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get CSRF token dynamically
            let itemId = this.id.split('remove_')[1];
            let size = this.getAttribute('data-size');
            let url = `/bag/remove/${itemId}`;
            let data = new FormData();
            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('size', size);

            fetch(url, {
                method: 'POST',
                body: data
            })
            .then(response => {
                if (response.ok) {
                    location.reload(); // Reload after successful removal
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
