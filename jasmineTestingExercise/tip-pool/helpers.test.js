describe("helpers test", function() {
    const billAmt = 100;
    const tipAmt = 25;
    it('should calculate the tip amount', function() {
        expect(calculateTipPercent(100, 25)).toEqual(25);
    });
    it('should calculate the total amount', function() {
        expect(calculateTotal(100, 25)).toEqual(125);
    });
    it('should append a new td element', function() {
        let tr = document.createElement('tr');
        appendTd(tr, 'test');
        expect(tr.children.length).toEqual(1);
        expect(tr.firstChild.innerHTML).toEqual('test');
    });
});