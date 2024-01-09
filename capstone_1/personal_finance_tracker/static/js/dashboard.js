document.addEventListener('DOMContentLoaded', function () {
    // Trigger the loadData function when the page loads
    loadData();

    // Toggles checkboxes on page load
    const allCheckboxCategories = document.querySelectorAll('.checkbox-categories input[type="checkbox"]');
    allCheckboxCategories.forEach(function (checkbox) {
        checkbox.checked = true;
        checkbox.addEventListener('change', loadData); // Add event listener for checkbox changes
    });

    // Add event listener for date change
    document.getElementById('selectDate').addEventListener('change', function () {
        loadData();
    });
    loadData();
});

function loadData() {
    const selectedDate = document.getElementById("selectDate").value;
    const selectedChartType = document.getElementById("chartType").value;

    // Get selected income categories
    const selectedIncomeCategories = getSelectedCategories('incomeCategory_');

    // Get selected expense categories
    const selectedExpenseCategories = getSelectedCategories('expenseCategory_');

    const url = `/load-data?date=${selectedDate}&chartType=${selectedChartType}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Filter data based on selected categories
            const filteredData = filterData(data, selectedIncomeCategories, selectedExpenseCategories);

            // Handle the received data and update the UI based on the selected chart type
            updateUI(filteredData, selectedChartType);
        })
        .catch(error => console.error('Error:', error));
}

// Helper function to get selected categories
function getSelectedCategories(prefix) {
    const selectedCategories = [];
    const checkboxes = document.querySelectorAll(`input[id^="${prefix}"]`);
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            selectedCategories.push(checkbox.value);
        }
    });
    return selectedCategories;
}

// Helper function to filter data based on selected categories
function filterData(data, selectedIncomeCategories, selectedExpenseCategories) {
    const filteredData = {
        income: data.income.filter(income => selectedIncomeCategories.includes(income.category)),
        expense: data.expense.filter(expense => selectedExpenseCategories.includes(expense.category))
    };
    return filteredData;
}

function updateUI(data, chartType) {
    const incomeList = document.getElementById("incomeList");
    const expenseList = document.getElementById("expenseList");

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
    const incomeChartData = [['Category', 'Amount']];
    data.income.forEach(function (income) {
        incomeChartData.push([income.category, income.amount]);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', { 'packages': ['corechart'] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function () {
        // Create the data table.
        const incomeDataTable = google.visualization.arrayToDataTable(incomeChartData);

        // Set chart options
        const options = {
            title: 'Income Distribution',
            width: 400,
            height: 300,
        };

        // Instantiate and draw the chart.
        const chart = new google.visualization.PieChart(document.getElementById('incomeChart'));
        chart.draw(incomeDataTable, options);
    });
}

function drawExpenseChart(data) {
    // Prepare data for the Expense Chart
    const expenseChartData = [['Category', 'Amount']];
    data.expense.forEach(function (expense) {
        expenseChartData.push([expense.category, expense.amount]);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', { 'packages': ['corechart'] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function () {
        // Create the data table.
        const expenseDataTable = google.visualization.arrayToDataTable(expenseChartData);

        // Set chart options
        const options = {
            title: 'Expense Distribution',
            width: 400,
            height: 300,
        };

        // Instantiate and draw the chart.
        const chart = new google.visualization.PieChart(document.getElementById('expenseChart'));
        chart.draw(expenseDataTable, options);
    });
}

function drawIncomeVsExpenseChart(data) {
    // Prepare data for the Income vs Expense Chart
    const incomeVsExpenseChartData = [['Category', 'Income', 'Expense']];
    data.income.forEach(function (income) {
        const correspondingExpense = data.expense.find(expense => expense.category === income.category);
        const expenseAmount = correspondingExpense ? correspondingExpense.amount : 0;
        incomeVsExpenseChartData.push([income.category, income.amount, expenseAmount]);
    });

    // Load the Visualization API and the corechart package.
    google.charts.load('current', { 'packages': ['corechart'] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function () {
        // Create the data table.
        const incomeVsExpenseDataTable = google.visualization.arrayToDataTable(incomeVsExpenseChartData);

        // Set chart options
        const options = {
            title: 'Income vs Expense',
            width: 400,
            height: 300,
            bars: 'vertical',
            vAxis: { format: 'currency' }
        };

        // Instantiate and draw the chart.
        const chart = new google.visualization.PieChart(document.getElementById('incomeVsExpenseChart'));
        chart.draw(incomeVsExpenseDataTable, options);
    });
}

// Remove flash message after 3 seconds
setTimeout(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        message.style.opacity = '0';
        setTimeout(function() {
            message.remove();
        }, 300); // remove the message after the transition is complete
    });
}, 3000); // 3000 milliseconds = 3 seconds
