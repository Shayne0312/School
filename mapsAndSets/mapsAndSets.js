// What does the following code return?
//new Set([1,1,2,2,3,4]) // {1,2,3,4}

// What does the following code return?
//[...new Set("referee")].join("") // 'ref'

// What does the Map m look like after running the following code?
//let m = new Map();
//m.set([1,2,3], true);
//m.set([1,2,3], false); // {Array(3) => true, Array(3) => false}

//Write a function called hasDuplicate which accepts an array and returns true or false if that array contains a duplicate
//hasDuplicate([1,3,2,1]) // true
//hasDuplicate([1,5,-1,4]) // false

//const hasDuplicate = arr => new Set(arr).size !== arr.length;

//Write a function called vowelCount which accepts a string and returns a map where the keys are numbers and the values are 
//the count of the vowels in the string.


const isVowel = char => 'aeiou'.includes(char);

const vowelCount = str => {
    const vowelMap = new Map();
    for(let char of str){
        let lowerCaseChar = char.toLowerCase()
        if(isVowel(lowerCaseChar)){
            if(vowelMap.has(lowerCaseChar)){
                vowelMap.set(lowerCaseChar, vowelMap.get(lowerCaseChar) + 1);
            } else {
                vowelMap.set(lowerCaseChar, 1);
            }
        }
    }
    return vowelMap;
}
console.log(vowelCount('awesome')) // Map { 'a' => 1, 'e' => 2, 'o' => 1 }
console.log(vowelCount('Colt')) // Map { 'o' => 1 }
