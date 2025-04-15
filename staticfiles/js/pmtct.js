// FAQ Toggle
document.querySelectorAll('.toggle-header').forEach(header => {
    header.addEventListener('click', () => {
        const contentId = header.getAttribute('data-toggle');
        const content = document.getElementById(contentId);
        const icon = header.querySelector('.toggle-icon');
        content.classList.toggle('active');
        icon.textContent = content.classList.contains('active') ? '▲' : '▼';
    });
});

// Hero Animation
document.addEventListener('DOMContentLoaded', () => {
    const heroText = document.querySelector('.about-hero-text');
    setTimeout(() => heroText.classList.add('visible'), 100);
});