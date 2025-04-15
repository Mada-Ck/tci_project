// Sidebar Toggle
document.querySelector('.sidebar-toggle').addEventListener('click', () => {
    const menu = document.querySelector('.sidebar-menu');
    const icon = document.querySelector('.sidebar-toggle .toggle-icon');
    menu.classList.toggle('active');
    icon.textContent = menu.classList.contains('active') ? '▲' : '▼';
});

// Content Toggle
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

// Executive Animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.2 });

document.querySelectorAll('.member-card').forEach(card => observer.observe(card));