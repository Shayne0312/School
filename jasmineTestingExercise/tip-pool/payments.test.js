describe("payments test", function() {
    
    it('should add a new payment to allPayments on submitPaymentInfo()', function() {
        billAmtInput.value = 100;
        tipAmtInput.value = 25;
        submitPaymentInfo();
        expect(Object.keys(allPayments).length).toEqual(1);
        expect(allPayments['payment1'].billAmt).toEqual('100');
        expect(allPayments['payment1'].tipAmt).toEqual('25');
        expect(allPayments['payment1'].tipPercent).toEqual(25);
    });
    it('should not add a new payment to allPayments on submitPaymentInfo() with negative billAmt', function() {
        billAmtInput.value = -100;
        tipAmtInput.value = 25;
        submitPaymentInfo();
        expect(Object.keys(allPayments).length).toEqual(0);
    });
    it('should create row and appendTD with input value', function() {
        let expectedPayment = {
            billAmt: '100',
            tipAmt: '20',
            tipPercent: 20,
          }
      
          expect(createCurPayment()).toEqual(expectedPayment);
        });
        it('should not create payment with empty input on createCurPayment()', function () {
            billAmtInput.value = '';
            tipAmtInput.value = '';
            let curPayment = createCurPayment();
        
            expect(curPayment).toEqual(undefined);
          });
        
          afterEach(function() {
            billAmtInput.value = '';
            tipAmtInput.value = '';
            paymentTbody.innerHTML = '';
            summaryTds[0].innerHTML = '';
            summaryTds[1].innerHTML = '';
            summaryTds[2].innerHTML = '';
            serverTbody.innerHTML = '';
            paymentId = 0;
            allPayments = {};
          });
        });