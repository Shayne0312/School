document.addEventListener('DOMContentLoaded', function () {
    // Toggles checkboxes on page load
    const allCheckboxCategories = document.querySelectorAll('.checkbox-categories input[type="checkbox"]');
    allCheckboxCategories.forEach(function (checkbox) {
        checkbox.checked = true;
        checkbox.addEventListener('change', loadData);
        loadData();
    });

    // Event listener for date change
    const selectDateElement = document.getElementById('selectDate');
    if (selectDateElement) {
        selectDateElement.addEventListener('change', function () {
            loadData();
        });
    }

    // Event listener for budget date deletion
    const deleteDateButtonElement = document.getElementById('deleteDateButton');
    if (deleteDateButtonElement) {
        deleteDateButtonElement.addEventListener('click', function () {
            deleteSelectedDate();
        });
    }

    loadData();
});


function loadData() {
    const selectedDateElement = document.getElementById("selectDate");

    // Check if the element exists before accessing its value
    if (!selectedDateElement) {
        // If the element doesn't exist, return without logging an error
        return;
    }

    const selectedDate = selectedDateElement.value;
    const selectedChartTypeElement = document.getElementById("chartType");
    const selectedChartType = selectedChartTypeElement ? selectedChartTypeElement.value : 'bar';

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
        .catch(error => error('Error:', error));

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
}


// Handles updating the UI after load data
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

    // Draw Income Chart with default type 'pie'
    drawIncomeChart(data, chartType || 'bar');

    // Draw Expense Chart with default type 'pie'
    drawExpenseChart(data, chartType || 'bar');

    // Draw Income vs Expense Chart with default type 'pie'
    drawIncomeVsExpenseChart(data, chartType || 'bar');
}

function updateSavingsUI(data) {
    const savingList = document.getElementById("savingList");

    // Clear previous data
    savingList.innerHTML = "<li>Savings Goals:</li>";

    // Display savings data
    data.saving.forEach(function (saving) {
        savingList.innerHTML += `<li>${saving.name} - ${saving.amount}</li>`;
    });
}

function deleteSelectedDate() {
    const selectedDate = document.getElementById("selectDate").value;

    // Confirm deletion with the user (you may customize this confirmation)
    const confirmDelete = confirm(`Are you sure you want to delete data for ${selectedDate}?`);

    if (confirmDelete) {
        // Send a request to the server to delete the selected date
        const url = `/delete-date?date=${selectedDate}`;

        fetch(url, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                // Reload the page after successful deletion
                location.reload();
            } else {
                console.error('Error deleting date:', response.status, response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function drawIncomeChart(data, chartType) {
    const incomeChartData = [['Category', 'Income']];
    data.income.forEach(function (income) {
        incomeChartData.push([income.category, income.amount]);
    });

    google.charts.load('current', { 'packages': ['corechart'] });

    google.charts.setOnLoadCallback(function () {
        const incomeDataTable = google.visualization.arrayToDataTable(incomeChartData);

        const options = {
            title: 'Income Distribution',
            width: 350,
            height: 300
        };

        let chart;

        switch (chartType) {
            case 'pie':
                chart = new google.visualization.PieChart(document.getElementById('incomeChart'));
                break;
            case 'line':
                chart = new google.visualization.LineChart(document.getElementById('incomeChart'));
                options.colors = ['green']; // Set color for other chart types
                break;
            case 'bar':
                chart = new google.visualization.BarChart(document.getElementById('incomeChart'));
                options.colors = ['green']; // Set color for other chart types
                break;
            case 'donut':
                chart = new google.visualization.PieChart(document.getElementById('incomeChart'));
                options.pieHole = 0.4;
                break;
        }

        if (chart) {
            chart.draw(incomeDataTable, options);
        }
    });
}

function drawExpenseChart(data, chartType) {
    const expenseChartData = [['Category', 'Expense']];
    data.expense.forEach(function (expense) {
        const expenseAmount = parseFloat(expense.amount);
        if (chartType === 'line' || chartType === 'bar') {
            expenseChartData.push([expense.category, -expenseAmount]);
        } else {
            expenseChartData.push([expense.category, expenseAmount]);
        }
    });

    google.charts.load('current', { 'packages': ['corechart'] });

    google.charts.setOnLoadCallback(function () {
        const expenseDataTable = google.visualization.arrayToDataTable(expenseChartData);

        const options = {
            title: 'Expense Distribution',
            width: 350,
            height: 300
        };

        let chart;

        switch (chartType) {
            case 'pie':
                chart = new google.visualization.PieChart(document.getElementById('expenseChart'));
                break;
            case 'line':
                chart = new google.visualization.LineChart(document.getElementById('expenseChart'));
                options.colors = ['red']; // Set color for other chart types
                break;
            case 'bar':
                chart = new google.visualization.BarChart(document.getElementById('expenseChart'));
                options.colors = ['red']; // Set color for other chart types
                break;
            case 'donut':
                chart = new google.visualization.PieChart(document.getElementById('expenseChart'));
                options.pieHole = 0.4;
                break;
        }

        if (chart) {
            chart.draw(expenseDataTable, options);
        }
    });
}

function drawIncomeVsExpenseChart(data, chartType) {
    // Prepare data for the IncomeVsExpense Chart
    const incomeVsExpenseChartData = [
        ['Category', 'Income', { role: 'annotation' }, 'Expense', { role: 'annotation' }],
    ];

    // Add income data
    data.income.forEach(function (income) {
        const categoryKey = income.category;
        const incomeAmount = parseFloat(income.amount);
        incomeVsExpenseChartData.push([categoryKey, incomeAmount, incomeAmount.toString(), 0, '']); // Positive value for income amount
    });

    // Add expense data
    data.expense.forEach(function (expense) {
        const categoryKey = expense.category;
        const expenseAmount = parseFloat(expense.amount);

        // Adjust expense amount based on chart type
        if (chartType === 'pie' || chartType === 'donut') {
            incomeVsExpenseChartData.push([categoryKey, expenseAmount, '', 0, expenseAmount.toString()]); // Positive value for expense amount
        } else {
            incomeVsExpenseChartData.push([categoryKey, 0, '', -expenseAmount, expenseAmount.toString()]); // Negative value for expense amount
        }
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
            width: 350,
            height: 300,
            vAxis: { format: 'currency' },
            series: {
                0: { color: 'green' }, // Positive amounts (green)
                2: { color: 'red' }    // Negative amounts (red)
            }
        };

        let chart;

        switch (chartType) {
            case 'pie':
                chart = new google.visualization.PieChart(document.getElementById('incomeVsExpenseChart'));
                break;
            case 'line':
                chart = new google.visualization.LineChart(document.getElementById('incomeVsExpenseChart'));
                break;
            case 'bar':
                chart = new google.visualization.BarChart(document.getElementById('incomeVsExpenseChart'));
                break;
            case 'donut':
                chart = new google.visualization.PieChart(document.getElementById('incomeVsExpenseChart'));
                options.pieHole = 0.4;
                break;
        }

        if (chart) {
            chart.draw(incomeVsExpenseDataTable, options);
        }
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
