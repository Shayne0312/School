// budgeting.js
function calculateBudget() {
    var salary = parseFloat(document.getElementById('salary').value) || 0;
    var otherIncome = parseFloat(document.getElementById('otherIncome').value) || 0;
    var investmentReturns = parseFloat(document.getElementById('investmentReturns').value) || 0;
    // Add other income sources as needed

    var housing = parseFloat(document.getElementById('housing').value) || 0;
    var utilities = parseFloat(document.getElementById('utilities').value) || 0;
    var food = parseFloat(document.getElementById('food').value) || 0;
    var transportation = parseFloat(document.getElementById('transportation').value) || 0;
    var insurance = parseFloat(document.getElementById('insurance').value) || 0;
    var healthcare = parseFloat(document.getElementById('healthcare').value) || 0;
    var savings = parseFloat(document.getElementById('savings').value) || 0;
    var entertainment = parseFloat(document.getElementById('entertainment').value) || 0;
    var childcare = parseFloat(document.getElementById('childcare').value) || 0;
    var debts = parseFloat(document.getElementById('debts').value) || 0;
    // Add other expense categories as needed

    var totalIncome = salary + otherIncome + investmentReturns; // Sum up all income sources
    var totalExpenses = housing + utilities + food + transportation + insurance + healthcare + savings + entertainment + childcare + debts; // Sum up all expenses

    var ctx = document.getElementById('budgetChart').getContext('2d');
    var budgetChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Total Income', 'Total Expenses'],
            datasets: [{
                label: 'Amount',
                data: [totalIncome, totalExpenses],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
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