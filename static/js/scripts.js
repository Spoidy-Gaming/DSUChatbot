document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded and scripts running.');

    // Example of a simple interactive feature: toggle card details
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Toggle 'active' class to show/hide more details
            card.classList.toggle('active');
            
            // Add/remove animation for the card content
            const content = card.querySelector('p');
            if (card.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
                content.style.transition = 'max-height 0.5s ease-in-out';
            } else {
                content.style.maxHeight = '0';
            }
        });
    });

    // Smooth scroll for any internal links (optional)
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Example for handling form submissions (if applicable)
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            // Send data to server or process it
            console.log('Form submitted:', Object.fromEntries(formData.entries()));
            // Display success message
            alert('Form submitted successfully!');
        });
    }
});
