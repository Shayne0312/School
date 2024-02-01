function addIncomeField() {
  const incomeFields = document.getElementById('income-fields');
  const newIncomeField = document.createElement('div');

  // Create input for category
  const categoryInput = document.createElement('input');
  categoryInput.type = 'text';
  categoryInput.name = 'income_entries[][category]';
  categoryInput.placeholder = 'Enter Category';
  newIncomeField.appendChild(categoryInput);

  // Create input for amount
  const amountInput = document.createElement('input');
  amountInput.type = 'number';
  amountInput.name = 'income_entries[][amount]';
  amountInput.placeholder = 'Enter Amount ($)';
  newIncomeField.appendChild(amountInput);
  incomeFields.appendChild(newIncomeField);
}

function addExpenseField() {
  const expenseFields = document.getElementById('expense-fields');
  const newExpenseField = document.createElement('div');

  // Create input for category
  const categoryInput = document.createElement('input');
  categoryInput.type = 'text';
  categoryInput.name = 'expense_entries[][category]';
  categoryInput.placeholder = 'Enter Category';
  newExpenseField.appendChild(categoryInput);

  // Create input for amount
  const amountInput = document.createElement('input');
  amountInput.type = 'number';
  amountInput.name = 'expense_entries[][amount]';
  amountInput.placeholder = 'Enter Amount ($)';
  newExpenseField.appendChild(amountInput);
  expenseFields.appendChild(newExpenseField);
}


// Function to prevent form submission
function preventFormSubmission(event) {
  event.preventDefault();
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
