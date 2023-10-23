
it('should calculate the monthly rate correctly', function () {
  const values = { amount: 10000, years: 8.0, rate: 5.0 };
  expect(calculateMonthlyPayment(values)).toEqual('126.60');
});

it('should return a result with 2 decimal places', function () {
  const values = { amount: 10000, years: 8.0, rate: 5.0 };
  const monthlyPayment = calculateMonthlyPayment(values);
  expect(monthlyPayment).toBeCloseTo(126.60, 2);
});

