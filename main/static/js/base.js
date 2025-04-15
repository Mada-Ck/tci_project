// Initialize small map
document.addEventListener('DOMContentLoaded', function () {
    // Small map
    var smallMap = L.map('map-small').setView([-9.7026, 33.2732], 10); // Chitipa, Malawi
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 18,
    }).addTo(smallMap);
    L.marker([-9.7026, 33.2732]).addTo(smallMap)
        .bindPopup('Thembi Community Initiative<br>Chitipa, Malawi')
        .openPopup();

    // Modal map
    var modalMap = null;
    var modal = document.getElementById('map-modal');
    var toggleMapBtn = document.getElementById('toggle-map');
    var closeBtn = document.querySelector('.close');

    if (toggleMapBtn && modal && closeBtn) {
        toggleMapBtn.addEventListener('click', function () {
            modal.style.display = 'flex';
            if (!modalMap) {
                modalMap = L.map('modal-map').setView([-9.7026, 33.2732], 10);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                    maxZoom: 18,
                }).addTo(modalMap);
                L.marker([-9.7026, 33.2732]).addTo(modalMap)
                    .bindPopup('Thembi Community Initiative<br>Chitipa, Malawi')
                    .openPopup();
            }
            setTimeout(function () {
                modalMap.invalidateSize();
            }, 100);
        });

        closeBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });

        window.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    // Set current year
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    // Theme toggle
    var themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var html = document.documentElement;
            var sunIcon = themeToggle.querySelector('.fa-sun');
            var moonIcon = themeToggle.querySelector('.fa-moon');
            if (html.getAttribute('data-theme') === 'light') {
                html.setAttribute('data-theme', 'dark');
                sunIcon.classList.add('d-none');
                moonIcon.classList.remove('d-none');
            } else {
                html.setAttribute('data-theme', 'light');
                sunIcon.classList.remove('d-none');
                moonIcon.classList.add('d-none');
            }
        });
    }

    // Hero carousel personalization
    const heroTitle = document.querySelector('.carousel-item.active .hero-title');
    if (heroTitle) {
        if (document.cookie.includes("visited=true")) {
            heroTitle.textContent = heroTitle.dataset.welcomeBack;
        } else {
            heroTitle.textContent = heroTitle.dataset.default;
            document.cookie = "visited=true; max-age=31536000";
        }
    }
});