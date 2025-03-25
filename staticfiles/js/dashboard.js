document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.section');
    const menuLinks = document.querySelectorAll('.dashboard-dropdown a');
    const formLinks = document.querySelectorAll('.sidebar a');
    const formSections = document.querySelectorAll('.form-section');

    // Helper function to hide all sections/forms
    function hideAll(elements) {
        elements.forEach(el => el.classList.remove('active'));
    }

    // Top Menu Links - Switch Sections
    menuLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            hideAll(sections);
            const targetSection = document.querySelector(`.${link.dataset.section}`);
            if (targetSection) targetSection.classList.add('active');
            // Hide dropdown after click
            document.querySelector('.dashboard-dropdown').style.display = 'none';
        });
    });

    // Show/hide dropdown on hover
    const menuIcon = document.querySelector('.menu-icon');
    menuIcon.addEventListener('mouseenter', () => {
        document.querySelector('.dashboard-dropdown').style.display = 'block';
    });
    menuIcon.addEventListener('mouseleave', () => {
        document.querySelector('.dashboard-dropdown').style.display = 'none';
    });

    // Sidebar Form Menu - Show specific form
    formLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            hideAll(formSections);
            const targetForm = document.querySelector(`.${link.dataset.form}`);
            if (targetForm) {
                targetForm.classList.add('active');
                document.querySelector('.form-content p').textContent =
                    `Close TA Mwaulambya - January 2025 - ${link.textContent}`;
            }
        });
    });

    // Initially hide all forms
    hideAll(formSections);

    // PivotTable.js Initialization with Plotly renderers
    const pivotScriptTag = document.getElementById('pivot-data');
    if (pivotScriptTag) {
        let pivotData;
        try {
            pivotData = JSON.parse(pivotScriptTag.textContent || '[]');
        } catch (e) {
            console.error("Failed to parse pivot data:", e);
            pivotData = [];
        }

        if (pivotData.length === 0) {
            $("#pivot-table-output").html("<p>No data available for pivot table.</p>");
            return;
        }

        // Detect all keys and numeric keys
        const allKeys = Object.keys(pivotData[0]);
        const numericKeys = allKeys.filter(key => typeof pivotData[0][key] === 'number');

        $("#pivot-table-output").pivotUI(
            pivotData,
            {
                rows: ["date", "period"].filter(k => allKeys.includes(k)),
                cols: [],
                vals: numericKeys.length > 0 ? [numericKeys[0]] : [],
                aggregatorName: "Sum",
                rendererName: "Table Barchart",
                renderers: $.extend(
                    $.pivotUtilities.renderers,
                    $.pivotUtilities.plotly_renderers || {}
                ),
                derivedAttributes: {
                    "Year": $.pivotUtilities.derivers.dateFormat("date", "%y"),
                    "Month": $.pivotUtilities.derivers.dateFormat("date", "%m")
                },
                rendererOptions: {
                    table: {
                        clickCallback: function (e, value, filters, pivotData) {
                            console.log("Clicked:", value, filters);
                        }
                    }
                }
            }
        );
    }
});