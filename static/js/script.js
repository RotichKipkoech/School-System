// General JavaScript for interactivity (if needed)

document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript is loaded and running!");

    // Example of a function for handling form submission or button click
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Form submitted!");
        });
    });
});
