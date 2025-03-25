document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const nav = document.querySelector('nav');
    const dropdowns = document.querySelectorAll('.dropdown');

    // Toggle mobile navigation
    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        nav.classList.toggle('active');
    });

    // Handle dropdowns on mobile
    dropdowns.forEach(dropdown => {
        const dropbtn = dropdown.querySelector('.dropbtn');
        if (window.innerWidth <= 768px) {
            dropbtn.addEventListener('click', function(e) {
                e.preventDefault();
                dropdown.classList.toggle('active');
            });
        }
    });

    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768) {
            dropdowns.forEach(dropdown => {
                if (!dropdown.contains(event.target)) {
                    dropdown.classList.remove('active');
                }
            });
        }
    });

    // Smooth scrolling and close mobile menu
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }

            if (hamburger && nav.classList.contains('active')) {
                nav.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    });

    // Dynamic Year in Footer
    const yearSpan = document.getElementById('currentYear');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // --- Expandable Info Cards (MODIFIED JavaScript) ---
    const infoCards = document.querySelectorAll('.info-card');

    infoCards.forEach(card => {
        const summary = card.querySelector('summary');
        const detailsContent = card.querySelector('.details-content');
        const infoCardRow = card.closest('.info-card-row'); // Get the parent row

        summary.addEventListener('click', (event) => {
            // Prevent the default <details> behavior
            event.preventDefault();

            const isExpanded = card.classList.contains('expanded'); // Check if card is currently expanded

            // Close all cards and remove expanded-card-present class from all rows initially
            infoCards.forEach(otherCard => {
                if (otherCard !== card) {
                    otherCard.classList.remove('expanded');
                    otherCard.querySelector('.details-content').style.maxHeight = '0px';
                }
            });
            document.querySelectorAll('.info-card-row').forEach(row => {
                row.classList.remove('expanded-card-present');
            });


            if (!isExpanded) { // If card was NOT expanded, now expand it
                // Expand the clicked card
                card.classList.add('expanded');
                detailsContent.style.maxHeight = detailsContent.scrollHeight + "px";
                infoCardRow.classList.add('expanded-card-present'); // Add class to parent row
            }
            // If card WAS expanded, collapsing is already handled above (all cards collapsed)
        });
    });
});