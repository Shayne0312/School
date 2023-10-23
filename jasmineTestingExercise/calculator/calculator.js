window.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("calc-form");
  if (form) {
    setupIntialValues();
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      update();
    });
  }
});

function getCurrentUIValues() {
  return {
    amount: +(document.getElementById("loan-amount").value),
    years: +(document.getElementById("loan-years").value),
    rate: +(document.getElementById("loan-rate").value),
  }
}

// Get the inputs from the DOM.
// Put some default values in the inputs
// Call a function to calculate the current monthly payment
function setupIntialValues() {
  const amount = +(document.getElementById("loan-amount").value);
  const years = +(document.getElementById("loan-years").value);
  const rate = +(document.getElementById("loan-rate").value);
  const values = { amount: amount, years: years, rate: rate };
  calculateMonthlyPayment(values);
  return values;
}

// Get the current values from the UI
// Update the monthly payment
function update() {
  const values = getCurrentUIValues();
  const monthly = calculateMonthlyPayment(values);
  updateMonthly(monthly);
}

// Given an object of values (a value has amount, years and rate ),
// calculate the monthly payment.  The output should be a string
// that always has 2 decimal places.
function calculateMonthlyPayment(values) {
  
    const p = values.amount;
    const i = (values.rate / 100) / 12;
    const n = Math.floor(values.years * 12);
  
    const monthly = (p * i) / (1 - (1 + i) ** -n);
    const monthlyStr = monthly.toFixed(2);
    return monthlyStr;
}

// Given a string representing the monthly payment value,
// update the UI to show the value.
function updateMonthly(monthly) {
  const monthlyPayment = document.getElementById("monthly-payment");
  monthlyPayment.innerText = "$" + monthly;
}
