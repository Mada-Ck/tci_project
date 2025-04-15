// Map Initialization
document.addEventListener('DOMContentLoaded', function () {
    // Initialize small map in footer
    const mapContainer = document.querySelector('.map-container');
    const toggleMapBtn = document.getElementById('toggle-map');
    const modal = document.getElementById('map-modal');
    const modalMapContainer = document.getElementById('modal-map');
    const closeModal = document.querySelector('.modal .close');

    if (mapContainer) {
        // Placeholder for small map (replace with actual map API like Google Maps or Leaflet)
        const smallMap = document.createElement('div');
        smallMap.style.width = '100%';
        smallMap.style.height = '100%';
        smallMap.style.backgroundColor = '#e0e0e0'; // Placeholder background
        smallMap.innerHTML = '<p style="text-align: center; line-height: 150px;">Small Map Placeholder</p>';
        mapContainer.appendChild(smallMap);
        mapContainer.classList.add('map-loaded');
    }

    // Toggle modal for larger map
    if (toggleMapBtn && modal && modalMapContainer) {
        toggleMapBtn.addEventListener('click', function () {
            modal.style.display = 'flex';
            document.body.classList.add('modal-open');

            // Initialize larger map in modal (replace with actual map API)
            const largeMap = document.createElement('div');
            largeMap.style.width = '100%';
            largeMap.style.height = '100%';
            largeMap.style.backgroundColor = '#e0e0e0'; // Placeholder background
            largeMap.innerHTML = '<p style="text-align: center; line-height: 400px;">Large Map Placeholder</p>';
            modalMapContainer.innerHTML = '';
            modalMapContainer.appendChild(largeMap);
        });
    }

    // Close modal
    if (closeModal && modal) {
        closeModal.addEventListener('click', function () {
            modal.style.display = 'none';
            document.body.classList.remove('modal-open');
        });

        // Close modal when clicking outside
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.classList.remove('modal-open');
            }
        });
    }
});