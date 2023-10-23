//ES5
// function filterOutOdds() {
//     var nums = Array.prototype.slice.call(arguments);
//     return nums.filter(function(num) {
//       return num % 2 === 0
//     });
//   }

//ES2015
const filterOutOdds = (...nums) => nums.filter((num) => num % 2 === 0);


// Write a function called findMin that accepts a variable number of 
// arguments and returns the smallest argument.
// Make sure to do this using the rest and spread operator.

const findMin = (...nums) => Math.min(...nums);
console.log(findMin(1, 4, 12, -3)); // -3
console.log(findMin(1, -1)); // -1
console.log(findMin(3, 1)); // 1

//*********************************************************************

// Write a function called mergeObjects that accepts two objects and returns a 
// new object which contains all the keys and values of the first object and 
// second object.

const obj1 = {a: 1, b: 2};
const obj2 = {c: 3, d: 4};

const mergeObjects = (obj1, obj2) => {
    return {...obj1, ...obj2};
};

const mergedObject = mergeObjects(obj1, obj2);
console.log(mergedObject);

//*********************************************************************

const doubleAndReturnArgs = (arr, ...val) => [...arr, ...val.map((num) => num * 2)];

console.log(doubleAndReturnArgs([1, 2, 3], 4, 4)); // [1, 2, 3, 8, 8]
console.log(doubleAndReturnArgs([2], 10, 4)); // [2, 20, 8]

//*********************************************************************

// Remove a random element in the items array
// and return a new array without that item.

const removeRandom = items => {
    let idx = Math.floor(Math.random() * items.length);
    return [...items.slice(0, idx), ...items.slice(idx + 1)];
  }
  const extend = (array1, array2) => {
    return [...array1, ...array2];
  }
    const addKeyVal = (obj, key, val) => {
    let newObj = { ...obj };
    newObj[key] = val;
    return newObj;
    }