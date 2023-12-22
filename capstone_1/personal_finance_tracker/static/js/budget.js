document.addEventListener('DOMContentLoaded', function() {
    const addIncomeButton = document.getElementById('addIncomeButton');
    const addExpenseButton = document.getElementById('addExpensesButton');

    if (addIncomeButton) {
        addIncomeButton.addEventListener('click', addIncome);
    }

    if (addExpenseButton) {
        addExpenseButton.addEventListener('click', addExpense);
    }
});

let incomeTotal = 0;
let expensesTotal = 0;

function addIncome() {
    addEntry('income');
}

function addExpense() {
    addEntry('expense');
}

function addEntry(type) {
    const categoryInput = document.querySelector(`select[name=${type}_category]`);
    const amountInput = document.querySelector(`input[name=${type}_amount]`);

    if (!categoryInput || !amountInput) {
        console.error('CategoryInput or AmountInput not found.');
        return;
    }

    const category = categoryInput.value;
    const amount = parseFloat(amountInput.value);

    if (isNaN(amount) || amount <= -1) {
        return;
    }

    const entryList = document.getElementById(`${type}List`);
    const newEntry = document.createElement('li');

    // Check the entry type and adjust the sign accordingly
    const sign = type === 'income' ? '' : '-';
    newEntry.textContent = `${category}: $${sign}${amount}`;
    entryList.appendChild(newEntry);

    // Update total values
    if (type === 'income') {
        incomeTotal += amount;
    } else {
        expensesTotal += amount;
    }

    // Update total elements
    updateTotalElements();

    // Clear input values after adding the entry
    amountInput.value = '';
}

function updateTotalElements() {
    const incomeTotalElement = document.getElementById('incomeTotal');
    const expensesTotalElement = document.getElementById('expensesTotal');
    const netTotalElement = document.getElementById('netTotal');

    incomeTotalElement.textContent = incomeTotal.toFixed(2);
    expensesTotalElement.textContent = expensesTotal.toFixed(2);

    // Calculate net total
    const netTotal = incomeTotal - expensesTotal;
    netTotalElement.textContent = netTotal.toFixed(2);
}
