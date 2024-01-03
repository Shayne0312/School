document.addEventListener('DOMContentLoaded', function () {
    // Trigger the loadData function when the page loads
    loadData();
});

function loadData() {
    var selectedDate = document.getElementById("selectDate").value;
    var url = `/load-data?date=${selectedDate}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Handle the received data and update the UI
            updateUI(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateUI(data) {
    // Update the UI with the received data (income, expense, etc.)
    // You can modify this part based on how you want to display the data
    console.log(data); // Log the data to the console for testing
}

function updateUI(data) {
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
}