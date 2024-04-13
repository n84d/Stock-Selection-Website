document.addEventListener('DOMContentLoaded', function() {
    // Fetch portfolio data from the server
    fetch('/portfolio-data')
        .then(response => response.json())
        .then(portfolio_data => {
            displayPortfolio(portfolio_data);
        })
        .catch(error => {
            console.error('Error fetching portfolio data:', error);
        });
});


function displayPortfolio(portfolio_data) {
    // Define function to create HTML table from DataFrame data
    function createTable(data) {
        const table = document.createElement('table');
        const headerRow = document.createElement('tr');
        const headerTicker = document.createElement('th');
        headerTicker.textContent = 'Ticker';
        headerTicker.style.color = 'black';
        const headerPrediction = document.createElement('th');
        headerPrediction.textContent = 'Prediction';
        headerPrediction.style.color = 'black';
        headerRow.appendChild(headerTicker);
        headerRow.appendChild(headerPrediction);
        table.appendChild(headerRow);

        data.forEach(row => {
            const tableRow = document.createElement('tr');
            const tickerCell = document.createElement('td');
            tickerCell.textContent = row['Ticker'];
            tickerCell.style.color = 'black';
            const predictionCell = document.createElement('td');
            predictionCell.textContent = row['Prediction'];
            predictionCell.style.color = 'black';
            // Check if prediction value is greater than 0.55
            if (parseFloat(row['Prediction']) > 0.55) {
                // Set background color to blue for rows with prediction > 0.55
                tableRow.style.backgroundColor = 'rgb(35, 52, 83)';
                // Set text color to white for better contrast
                tickerCell.style.color = 'white';
                predictionCell.style.color = 'white';
            } else {
                tableRow.style.backgroundColor = 'rgb(162, 213, 255)';
            }
            tableRow.appendChild(tickerCell);
            tableRow.appendChild(predictionCell);
            table.appendChild(tableRow);
        });
        return table;
    }

    // Display portfolio data based on button click
    function displayPortfolioTable(quarter) {
        if (currentPortfolio === quarter) {
            // If the same button is clicked again, hide the portfolio
            portfolioContainer.innerHTML = '';
            currentPortfolio = null;
        } else {
            // Otherwise, display the portfolio for the selected quarter
            portfolioContainer.innerHTML = '';
            portfolioContainer.appendChild(createTable(portfolio_data[quarter]));
            currentPortfolio = quarter;
        }
    }

    // Get HTML elements
    const q4_2023Button = document.getElementById('23q4-button');
    const q1_2024Button = document.getElementById('24q1-button');
    const q2_2024Button = document.getElementById('24q2-button');
    const portfolioContainer = document.getElementById('portfolio-container');

    let currentPortfolio = null;

    // Event listeners for quarter buttons
    q4_2023Button.addEventListener('click', () => displayPortfolioTable(0));
    q1_2024Button.addEventListener('click', () => displayPortfolioTable(1));
    q2_2024Button.addEventListener('click', () => displayPortfolioTable(2));
}
