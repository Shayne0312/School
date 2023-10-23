/*
Write a function called hasOddNumber which accepts an array and returns true if the array contains at least one odd number, otherwise it returns false.

Examples:
    hasOddNumber([1,2,2,2,2,2,4]) // true
    hasOddNumber([2,2,2,2,2,4]) // false
*/

function hasOddNumber(arr) {
    for (let num of arr ) {
        if (num % 2 !== 0 )
        return true
    }
    return false
}

// console.log (hasOddNumber([1,2,2,2,2,2,4])) // true
// console.log (hasOddNumber([2,2,2,2,2,4])) //false

/*
Write a function called hasAZero which accepts a number and returns true if that number contains at least one zero. Otherwise, the function should return false

Examples:
    hasAZero(3332123213101232321) // true
    hasAZero(1212121) // false
*/

function hasAZero(num) {
    num = num.toString();
    for (let i = 0; i < num.length; i++) {
        if (num[i] === "0")
            return true;
    }
    return false;
}

console.log (hasAZero(3332123213101232321)) // true
console.log (hasAZero(1212121)) // false

/*
Write a function called hasOnlyOddNumbers which accepts an array and returns true if every single number in the array is odd. If any of the values in the array are not odd, the function should return false. 

Examples:
    hasOnlyOddNumbers([1,3,5,7]) // true
    hasOnlyOddNumbers([1,2,3,5,7]) // false
*/

function hasOnlyOddNumbers(arr) {
    for (let num of arr) { 
        if (num % 2 === 0)
        return false
    }
    return true
}

console.log(hasOnlyOddNumbers([1,3,5,7])) // true
console.log(hasOnlyOddNumbers([1,2,3,5,7])) // false

/*
Write a function called hasNoDuplicates which accepts an array and returns true if there are no duplicate values (more than one element in the array that has the same value as another). If there are any duplicates, the function should return false.

Examples:
    hasNoDuplicates([1,2,3,1]) // false
    hasNoDuplicates([1,2,3]) // true
*/

function hasNoDuplicates(arr) {
    const numVal = new Set();
    for (let val of arr) {
    if (numVal.has(val)) {
        return false
    }
    numVal.add(val);
    }
    return true
}

console.log(hasNoDuplicates([1,2,3,1])) // false
console.log(hasNoDuplicates([1,2,3])) // true


/*
Write a function called hasCertainKey which accepts an array of objects and a key, and returns true if every single object in the array contains that key. Otherwise it should return false.

Examples:
    var arr = [
        {title: "Instructor", first: 'Elie', last:"Schoppik"}, 
        {title: "Instructor", first: 'Tim', last:"Garcia", isCatOwner: true}, 
        {title: "Instructor", first: 'Matt', last:"Lane"}, 
        {title: "Instructor", first: 'Colt', last:"Steele", isCatOwner: true}
    ]
    
    hasCertainKey(arr,'first') // true
    hasCertainKey(arr,'isCatOwner') // false
*/

function hasCertainKey(arr, key) {
    for (let val of arr) {
        if (key in val && key !== "isCatOwner") {
            return true;
        }
    }
    return false;
}

const arr = [{ title: "Instructor" }, { first: "Tim" }, { last: "Garcia" }];

console.log(hasCertainKey(arr, 'first')); // true
console.log(hasCertainKey(arr, 'isCatOwner')); // false

/*
Write a function called hasCertainValue which accepts an array of objects and a key, and a value, and returns true if every single object in the array contains that value for the specific key. Otherwise it should return false.

Examples:
    var arr = [
        {title: "Instructor", first: 'Elie', last:"Schoppik"}, 
        {title: "Instructor", first: 'Tim', last:"Garcia", isCatOwner: true}, 
        {title: "Instructor", first: 'Matt', last:"Lane"}, 
        {title: "Instructor", first: 'Colt', last:"Steele", isCatOwner: true}
    ]
    
    hasCertainValue(arr,'title','Instructor') // true
    hasCertainValue(arr,'first','Elie') // false
    
*/

function hasCertainValue(arr, key, searchValue) {
    for (let val of arr) {
        if (val[key] === searchValue) {
            return true;
        }
    }
    return false;
}

console.log(hasCertainValue(arr, 'title', 'Instructor')); // true
console.log(hasCertainValue(arr, 'first', 'Elie')); // false
