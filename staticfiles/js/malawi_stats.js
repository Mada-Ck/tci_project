document.addEventListener('DOMContentLoaded', function () {
    var unaidsData = [{
        type: 'bar',
        x: [95, 91, 87],
        y: ['Know Their Status', 'On Treatment', 'Virally Suppressed'],
        orientation: 'h',
        marker: {
            color: '#1a3c7e',
            line: { color: '#153267', width: 2 }
        },
        text: ['95%', '91%', '87%'],
        textposition: 'auto',
        hoverinfo: 'text',
        hovertext: [
            '95% of 991,600 PLHIV know their status: 941,020',
            '91% of diagnosed on treatment: 927,310',
            '87% of those on ART virally suppressed: 852,301'
        ]
    }];

    var unaidsLayout = {
        title: {
            text: 'Malawi\'s Progress Towards UNAIDS 95-95-95 Targets (2023)',
            font: { size: 18, color: '#1a3c7e', family: 'Montserrat, sans-serif' }
        },
        xaxis: {
            title: 'Percentage Achieved (%)',
            range: [0, 100],
            titlefont: { color: '#4a5568', family: 'Open Sans, sans-serif' },
            tickfont: { color: '#4a5568', family: 'Open Sans, sans-serif' }
        },
        yaxis: {
            title: 'UNAIDS Targets',
            titlefont: { color: '#4a5568', family: 'Open Sans, sans-serif' },
            tickfont: { color: '#4a5568', family: 'Open Sans, sans-serif' }
        },
        margin: { t: 50, b: 50, l: 120, r: 50 },
        height: 400,
        plot_bgcolor: '#fff',
        paper_bgcolor: '#fff',
        showlegend: false,
        hovermode: 'closest'
    };

    Plotly.newPlot('unaids-chart', unaidsData, unaidsLayout);
});