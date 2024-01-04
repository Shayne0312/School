document.addEventListener('DOMContentLoaded', function () {
    // Trigger the loadData function when the page loads
    loadData();
});

function loadData() {
    var selectedDate = document.getElementById("selectDate").value;
    var selectedChartType = document.getElementById("chartType").value;
    var url = `/load-data?date=${selectedDate}&chartType=${selectedChartType}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Handle the received data and update the UI based on the selected chart type
            updateUI(data, selectedChartType);
        })
        .catch(error => console.error('Error:', error));
}

function updateUI(data, chartType) {
    var incomeList = document.getElementById("incomeList");
    var expenseList = document.getElementById("expenseList");

    // Clear previous data
    incomeList.innerHTML = "<li>Income:</li>";
    expenseList.innerHTML = "<li>Expenses:</li>";

    // Display income data
    data.income.forEach(function (income) {
        incomeList.innerHTML += `<li>${income.category} - ${income.amount}</li>`;
    });

    // Display expense data
    data.expense.forEach(function (expense) {
        expenseList.innerHTML += `<li>${expense.category} - ${expense.amount}</li>`;
    });

    // Draw Income Chart
    drawIncomeChart(data);

    // Draw Expense Chart
    drawExpenseChart(data);

    // Draw Income vs Expense Chart
    drawIncomeVsExpenseChart(data);
}

function drawIncomeChart(data) {
    // Prepare data for the Income Chart
    var incomeChartData = [['Category', 'Amount']];
    data.income.forEach(function (income) {
        incomeChartData.push([income.category, income.amount]);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', { 'packages': ['corechart'] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function () {
        // Create the data table.
        var incomeDataTable = google.visualization.arrayToDataTable(incomeChartData);

        // Set chart options
        var options = {
            title: 'Income Distribution',
            width: 400,
            height: 300,
        };

        // Instantiate and draw the chart.
        var chart = new google.visualization.PieChart(document.getElementById('incomeChart'));
        chart.draw(incomeDataTable, options);
    });
}

function drawExpenseChart(data) {
    // Prepare data for the Expense Chart
    var expenseChartData = [['Category', 'Amount']];
    data.expense.forEach(function (expense) {
        expenseChartData.push([expense.category, expense.amount]);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', { 'packages': ['corechart'] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function () {
        // Create the data table.
        var expenseDataTable = google.visualization.arrayToDataTable(expenseChartData);

        // Set chart options
        var options = {
            title: 'Expense Distribution',
            width: 400,
            height: 300,
        };

        // Instantiate and draw the chart.
        var chart = new google.visualization.PieChart(document.getElementById('expenseChart'));
        chart.draw(expenseDataTable, options);
    });
}

function drawIncomeVsExpenseChart(data) {
    // Prepare data for the Income vs Expense Chart
    var incomeVsExpenseChartData = [['Category', 'Income', 'Expense']];
    data.income.forEach(function (income) {
        var correspondingExpense = data.expense.find(expense => expense.category === income.category);
        var expenseAmount = correspondingExpense ? correspondingExpense.amount : 0;
        incomeVsExpenseChartData.push([income.category, income.amount, expenseAmount]);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', { 'packages': ['corechart'] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function () {
        // Create the data table.
        var incomeVsExpenseDataTable = google.visualization.arrayToDataTable(incomeVsExpenseChartData);

        // Set chart options
        var options = {
            title: 'Income vs Expense',
            width: 400,
            height: 300,
            bars: 'vertical',
            vAxis: { format: 'currency' }
        };

        // Instantiate and draw the chart.
        var chart = new google.visualization.PieChart(document.getElementById('incomeVsExpenseChart'));
        chart.draw(incomeVsExpenseDataTable, options);
    });
}
