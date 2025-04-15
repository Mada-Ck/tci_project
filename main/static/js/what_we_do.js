// Hero Animation
document.addEventListener('DOMContentLoaded', () => {
    const heroText = document.querySelector('.about-hero-text');
    setTimeout(() => heroText.classList.add('visible'), 100);
});

// Form Submission Feedback (Optional)
document.querySelector('.subscription-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for subscribing! We’ll keep you updated.');
    e.target.reset();
});