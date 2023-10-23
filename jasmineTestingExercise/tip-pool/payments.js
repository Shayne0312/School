document.addEventListener('DOMContentLoaded', function() {
  let billAmtInput = document.getElementById('billAmt');
  let tipAmtInput = document.getElementById('tipAmt');
  let paymentForm = document.getElementById('paymentForm');
  let createCurPayment = document.getElementById('createCurPayment');
  let paymentTbody = document.querySelector('#paymentTable tbody');
  let summaryTds = document.querySelectorAll('#summaryTable tbody tr td');

  let allPayments = {};
  let paymentId = 0;

  paymentForm.addEventListener('submit', submitPaymentInfo);

  function createCurPayment() {
    let billAmt = billAmtInput.value;
    let tipAmt = tipAmtInput.value;

    if (billAmt === '' || tipAmt === '') return;

    if (Number(billAmt) > 0 && Number(tipAmt) >= 0) {
      return {
        billAmt: billAmt,
        tipAmt: tipAmt,
        tipPercent: calculateTipPercent(billAmt, tipAmt),
      };
    }
  }

  function submitPaymentInfo(evt) {
    if (evt) evt.preventDefault();

    let curPayment = createCurPayment();

    if (curPayment) {
      paymentId += 1;

      allPayments['payment' + paymentId] = curPayment;

      appendPaymentTable(curPayment);
      updateServerTable();
      updateSummary();

      billAmtInput.value = '';
      tipAmtInput.value = '';
    }
  }

  function appendPaymentTable(curPayment) {
    let billAmt = billAmtInput.value;
    let tipAmt = tipAmtInput.value;
    let tipPercent = calculateTipPercent(billAmt, tipAmt);
    let newTr = document.createElement('tr');
    newTr.id = 'payment' + paymentId;

    appendTd(newTr, '$' + curPayment.billAmt);
    appendTd(newTr, '$' + curPayment.tipAmt);
    appendTd(newTr, curPayment.tipPercent + '%');

    paymentTbody.append(newTr);
  }

  function updateSummary() {
    let tipPercentAvg;
    let paymentTotal = sumPaymentTotal('tipPercent');
    let numberOfPayments = Object.keys(allPayments).length;

    if (paymentTotal === 0 && numberOfPayments === 0) {
      tipPercentAvg = 0;
    } else {
      tipPercentAvg = paymentTotal / numberOfPayments;
    }

    summaryTds[0].innerHTML = '$' + sumPaymentTotal('billAmt');
    summaryTds[1].innerHTML = '$' + sumPaymentTotal('tipAmt');
    summaryTds[2].innerHTML = Math.round(tipPercentAvg) + '%';
  }
});