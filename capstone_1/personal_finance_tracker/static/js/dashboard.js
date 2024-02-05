// This event listener ensures that the DOM content is fully loaded before executing the code
document.addEventListener('DOMContentLoaded', async function () {
    // Elements for date selection and deletion
    const selectSavingsDateElement = document.getElementById('selectSavingsDate');
    const deleteSavingsDateButtonElement = document.getElementById('deleteSavingsDate');
    const selectDateElement = document.getElementById('selectDate');
    const deleteDateButtonElement = document.getElementById('deleteDateButton');

    // Add event listeners for date deletion
    if (deleteDateButtonElement) {
        deleteDateButtonElement.addEventListener('click', deleteSelectedDate);
    }

    if (deleteSavingsDateButtonElement) {
        deleteSavingsDateButtonElement.addEventListener('click', deleteSelectedSavingsDate);
    }

    // Add event listener for date change to trigger category and data loading
    selectDateElement.addEventListener('change', async function () {
        await loadCategoriesAndData();
        await loadSavingDataAndCalculateSavings();
    });

    // Initial loading of categories and data
    await loadCategoriesAndData();
    await loadSavingDataAndCalculateSavings();
});

// Function to load categories and data
async function loadCategoriesAndData() {
    try {
        await loadCategories();
        await loadData();
    } catch (error) {
        console.error('Error loading categories and data:', error.message);
    }
}

// Function to fetch and load categories
async function loadCategories() {
    try {
        const selectedDateElement = document.getElementById('selectDate');
        if (!selectedDateElement) {
            throw new Error('Element with ID \'selectDate\' not found.');
        }

        const selectedDate = selectedDateElement.value;
        const response = await fetch(`/get-categories?date=${selectedDate}`);
        const data = await response.json();

        renderCategories(data);
    } catch (error) {
        console.error('Error fetching categories:', error.message);
    }
}

// Function to render checkbox categories in the UI
function renderCategories(data) {
    const incomeDropdown = document.getElementById('incomeDropdownContent');
    const expenseDropdown = document.getElementById('expenseDropdownContent');

    incomeDropdown.innerHTML = '';
    expenseDropdown.innerHTML = '';

    // Render checkbox categories for income and expense
    renderCheckboxCategories(data.income_categories, incomeDropdown, 'incomeCategory_');
    renderCheckboxCategories(data.expense_categories, expenseDropdown, 'expenseCategory_');
}

// Function to render checkbox categories
function renderCheckboxCategories(categories, container, idPrefix) {
    container.innerHTML = categories.map(category => `
        <div class="checkbox-categories">
            <input type="checkbox" class="category-checkbox" value="${category}" id="${idPrefix}${category}" checked>
            ${category}
        </div>`
    ).join('');

    // Add change event listener for checkboxes to trigger data loading
    container.addEventListener('change', function (event) {
        if (event.target.classList.contains('category-checkbox')) {
            loadData(); // Call loadData when a checkbox changes

            // Optionally, you can also call loadSavingDataAndCalculateSavings here
            loadSavingDataAndCalculateSavings();
        }
    });
}

// Function to fetch and load data
async function loadData() {
    try {
        const selectedDateElement = document.getElementById('selectDate');

        // Check if the element exists
        if (!selectedDateElement) {
            return { income: [], expense: [] };
        }

        const selectedDate = selectedDateElement.value;
        const selectedChartTypeElement = document.getElementById('chartType');
        const selectedChartType = selectedChartTypeElement ? selectedChartTypeElement.value : 'bar';

        const selectedIncomeCategories = getSelectedCategories('incomeCategory_');
        const selectedExpenseCategories = getSelectedCategories('expenseCategory_');

        const url = `/load-data?date=${selectedDate}&chartType=${selectedChartType}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Error loading data: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        // Ensure that the loaded data object has both 'income' and 'expense' properties
        const loadedData = {
            income: data.income || [],
            expense: data.expense || []
        };

        // Filter data based on selected categories
        const filteredData = filterData(loadedData, selectedIncomeCategories, selectedExpenseCategories);
        updateUI(filteredData, selectedChartType);

        return loadedData; // Return the loaded data object
    } catch (error) {
        console.error('Error in loadData:', error);
        return { income: [], expense: [] }; // Return empty data structure in case of an error
    }

    // Helper function to get selected categories from checkboxes
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

// Function to fetch saving data and calculate savings potential
async function loadSavingDataAndCalculateSavings() {
    try {
        const data = await loadData(); // Ensure that the latest data is loaded
        const savingData = await loadSavingData();
        if (data && savingData) {
            const savingsPotentials = calculateSavingsPotential(data, savingData);
            displayRecommendation(savingsPotentials, savingData);

            // Call updateSavingsUI after loading saving data
            updateSavingsUI(savingData);

            return savingData; // Return the loaded saving data
        } else {
            console.error('Error: Data or savingData is undefined');
            return []; // Return empty array in case of an error
        }
    } catch (error) {
        console.error('Error in loadSavingDataAndCalculateSavings:', error);
        return []; // Return empty array in case of an error
    }
}

// Function to fetch saving data
async function loadSavingData() {
    try {
        const selectedSavingsDateElement = document.getElementById('selectSavingsDate');

        // Check if the element exists
        if (!selectedSavingsDateElement) {
            return [];
        }

        const selectedSavingsDate = selectedSavingsDateElement.value;
        const url = `/load-saving-data?saving-date=${selectedSavingsDate}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Error loading saving data: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        // Ensure that the loaded data object has a saving property
        return data.saving || [];
    } catch (error) {
        console.error('Error in loadSavingData:', error);
        return []; // Return empty array in case of an error
    }
}

// Function to update UI elements with data
function updateUI(data, chartType) {
    // Display data in UI
    displayDataList('incomeList', 'Income:', data.income);
    displayDataList('expenseList', 'Expenses:', data.expense);

    // Draw charts
    drawChart(data.income, 'Income Distribution', 'incomeChart', chartType, 'green');
    drawChart(data.expense, 'Expense Distribution', 'expenseChart', chartType, 'red');

    // Draw Income vs Expense Chart
    drawIncomeVsExpenseChart(data, chartType);

    // Display recommendation
    displayRecommendation(data.saving);
}

// Function to update savings UI elements with data
function updateSavingsUI(savingData) {
    // Display savings data in UI
    displayDataList('savingList', '', savingData);
}

// Function to display data in a list
function displayDataList(elementId, label, dataList) {
    const dataElement = document.getElementById(elementId);

    // Check if the element exists
    if (!dataElement) {
        console.error(`Element with ID '${elementId}' not found.`);
        return;
    }

    // Clear the existing content
    dataElement.innerHTML = "";

    // Append new data
    dataList.forEach(item => {
        dataElement.innerHTML += `<li>${label} ${item.category} - ${item.amount}</li>`;
    });
}

// Function to calculate savings potential based on income, expense, and saving data
function calculateSavingsPotential(data, savingData) {
    const totalIncome = data && data.income ? data.income.reduce((sum, income) => sum + parseFloat(income.amount), 0) : 0;
    const totalExpense = data && data.expense ? data.expense.reduce((sum, expense) => sum + parseFloat(expense.amount), 0) : 0;
    const totalSavings = savingData ? savingData.reduce((sum, saving) => sum + parseFloat(saving.amount), 0) : 0;

    let totalBudget = totalIncome - totalExpense;
    let monthlySavingsPotential = totalBudget;
    let monthsToAchieveGoal = (totalSavings / monthlySavingsPotential);

    return { monthlySavingsPotential, monthsToAchieveGoal };
}

// Function to display savings recommendation in the UI
function displayRecommendation(savingsPotentials) {
    try {
        const monthlySavingsPotientail = document.getElementById('monthlySavingsPotientailMessage');

        if (!monthlySavingsPotientail) {
            console.error('Element with ID \'monthlySavingsPotientailMessage\' not found.');
            return;
        }

        if (savingsPotentials && savingsPotentials.monthlySavingsPotential !== undefined) {
            const monthlySavingsPotentialCeiled = Math.ceil(savingsPotentials.monthlySavingsPotential);

            let monthsToAchieveGoal = savingsPotentials.monthsToAchieveGoal;

            // Check if monthsToAchieveGoal has a decimal part
            if (monthsToAchieveGoal % 1 !== 0) {
                monthsToAchieveGoal = monthsToAchieveGoal.toFixed(2);
            }

            const monthlySavingsPotientailMessage = `Your monthly saving potential is $ ${monthlySavingsPotentialCeiled}. Feel free to adjust this by creating a new budget and selecting the data.`;

            // Update the message in the HTML
            const recommendationMessage = `Your current budget of $${monthlySavingsPotentialCeiled}, you will achieve your savings goal in ${monthsToAchieveGoal} months.`;
            monthlySavingsPotientail.innerHTML = `<li>${recommendationMessage}</li>`;
            monthlySavingsPotientail.innerHTML += `<li>${monthlySavingsPotientailMessage}</li>`;

        } else {
            // Handle the case where monthly savings potential is undefined or non-positive
            monthlySavingsPotientail.innerHTML = `<li>Savings data is not available. Adjust your budget to save more.</li>`;
        }
    } catch (error) {
        console.error('Error in displayRecommendation:', error);
    }
}

// Function to display data in a specific element
function displayData(elementId, label, dataList) {
    const dataElement = document.getElementById(elementId);
    dataElement.innerHTML = `<li>${label}</li>`;
    dataList.forEach(item => {
        dataElement.innerHTML += `<li>${item.category} - ${item.amount}</li>`;
    });
}

// Function to draw a chart using Google Charts
function drawChart(data, title, chartId, chartType, color) {
    const chartData = [['Category', 'Amount']];
    data.forEach(item => {
        chartData.push([item.category, parseFloat(item.amount)]);
    });

    google.charts.load('current', { 'packages': ['corechart'] });

    google.charts.setOnLoadCallback(function () {
        const chartDataTable = google.visualization.arrayToDataTable(chartData);

        const options = {
            title: title,
            width: 350,
            height: 300,
            colors: [color]
        };

        let chart;

        // Create a chart based on the specified chart type
        switch (chartType) {
            case 'pie':
                chart = new google.visualization.PieChart(document.getElementById(chartId));
                break;
            case 'line':
                chart = new google.visualization.LineChart(document.getElementById(chartId));
                break;
            case 'bar':
                chart = new google.visualization.BarChart(document.getElementById(chartId));
                break;
            case 'donut':
                chart = new google.visualization.PieChart(document.getElementById(chartId));
                options.pieHole = 0.4;
                break;
        }

        // Draw the chart
        if (chart) {
            chart.draw(chartDataTable, options);
        }
    });
}

// Function to draw the Income vs Expense chart
function drawIncomeVsExpenseChart(data, chartType) {
    const incomeCategories = data.income.map(income => income.category);
    const expenseCategories = data.expense.map(expense => expense.category);
    const allCategories = Array.from(new Set([...incomeCategories, ...expenseCategories]));

    const incomeData = allCategories.map(category => {
        const incomeItem = data.income.find(income => income.category === category);
        return incomeItem ? parseFloat(incomeItem.amount) : 0;
    });

    const expenseData = allCategories.map(category => {
        const expenseItem = data.expense.find(expense => expense.category === category);
        return expenseItem ? parseFloat(expenseItem.amount) : 0;
    });

    const chartData = [['Category', 'Income', 'Expense']];
    allCategories.forEach((category, index) => {
        chartData.push([category, incomeData[index], expenseData[index]]);
    });

    google.charts.load('current', { 'packages': ['corechart'] });

    google.charts.setOnLoadCallback(function () {
        const incomeVsExpenseDataTable = google.visualization.arrayToDataTable(chartData);

        const options = {
            title: 'Income vs Expense',
            width: 350,
            height: 300,
            vAxis: { format: 'currency' },
            series: {
                0: { color: 'green' }, // Income (green)
                1: { color: 'red' }    // Expense (red)
            },
            isStacked: true
        };

        let chart;

        // Create a chart based on the specified chart type
        switch (chartType) {
            case 'line':
                chart = new google.visualization.LineChart(document.getElementById('incomeVsExpenseChart'));
                break;
            case 'bar':
                chart = new google.visualization.BarChart(document.getElementById('incomeVsExpenseChart'));
                break;
        }

        // Draw the chart
        if (chart) {
            chart.draw(incomeVsExpenseDataTable, options);
        }
    });
}

// Function to delete selected date
function deleteSelectedDate() {
    const selectedDate = document.getElementById('selectDate').value;
    const confirmDelete = confirm(`Are you sure you want to delete data for ${selectedDate}?`);

    if (confirmDelete) {
        const url = `/delete-date?date=${selectedDate}`;

        fetch(url, {
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error('Error deleting date:', response.status, response.statusText);
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

// Function to delete selected savings date
function deleteSelectedSavingsDate() {
    const selectedSavingDate = document.getElementById('selectSavingsDate').value;
    const confirmDelete = confirm(`Are you sure you want to delete savings data for ${selectedSavingDate}?`);

    if (confirmDelete) {
        const url = `/delete-saving-date?date=${selectedSavingDate}`;

        fetch(url, {
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    throw new Error(`Error deleting savings date: ${response.status} - ${response.statusText}`);
                }
            })
            .catch(error => console.error(error));
    }
}

// Remove flash message after 3 seconds
setTimeout(function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (message) {
        message.style.opacity = '0';
        setTimeout(function () {
            message.remove();
        }, 300); // remove the message after the transition is complete
    });
}, 3000); // 3000 milliseconds = 3 seconds
