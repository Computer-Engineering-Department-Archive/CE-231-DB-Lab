async function fetchData(url, method='GET', body=null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: body ? JSON.stringify(body) : null
    };
    const response = await fetch(url, options);
    const data = await response.json();
    return data;
}

async function generateNewLinks() {
    document.getElementById('loading-new-links').style.display = 'block';
    const newLinksData = await fetchData('/api/new-links');
    document.getElementById('loading-new-links').style.display = 'none';

    const newLinksChart = new Chart(document.getElementById('newLinksChart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: newLinksData.dates,
            datasets: [{
                label: 'New Links',
                data: newLinksData.counts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function generateVisits() {
    document.getElementById('loading-visits').style.display = 'block';
    const visitsData = await fetchData('/api/visits');
    document.getElementById('loading-visits').style.display = 'none';

    const visitsChart = new Chart(document.getElementById('visitsChart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: visitsData.dates,
            datasets: [{
                label: 'Visits',
                data: visitsData.counts,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function generateTopLinks() {
    document.getElementById('loading-top-links').style.display = 'block';
    const topLinksData = await fetchData('/api/top-links');
    document.getElementById('loading-top-links').style.display = 'none';

    const topLinksChart = new Chart(document.getElementById('topLinksChart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: topLinksData.links,
            datasets: [{
                label: 'Visits',
                data: topLinksData.counts,
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function loadStatistics() {
    generateNewLinks();
    generateVisits();
    generateTopLinks();
}

document.getElementById('url-stats-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const url = document.getElementById('url-input').value;
    window.location.href = `/url-stats/${url}`;
});

document.addEventListener('DOMContentLoaded', loadStatistics);
