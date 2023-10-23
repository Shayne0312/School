/* 
Write a function called `findUserByUsername` which accepts an array of objects, each with a key of username, and a string. The function should return the first object with the key of username that matches the string passed to the function. If the object is not found, return undefined. 
*/
const users = [
  {username: 'mlewis'},
  {username: 'akagen'},
  {username: 'msmith'}
];
/*
findUserByUsername(users, 'mlewis') // {username: 'mlewis'}
findUserByUsername(users, 'taco') // undefined
*/


function findUserByUsername(usersArray, username) {
  for (let i = 0; i < usersArray.length; i++) {
    if (usersArray[i].username === username) {
      return usersArray[i];
    }
  }
  return undefined;
}

console.log(findUserByUsername(users, 'mlewis')); // {username: 'mlewis'}
console.log(findUserByUsername(users, 'taco')); // undefined

/*
Write a function called `removeUser` which accepts an array of objects, each with a key of username, and a string. The function should remove the object from the array. If the object is not found, return undefined. 

const users = [
  {username: 'mlewis'},
  {username: 'akagen'},
  {username: 'msmith'}
];

removeUser(users, 'akagen') // {username: 'akagen'}
removeUser(users, 'akagen') // undefined
*/

function removeUser(usersArray, username) {
  for (let i = 0; i < usersArray.length; i++) {
    if (usersArray[i].username === username) {
      return usersArray.splice(i, 1)[0];
    }
  }
  return undefined;
}

console.log (removeUser(users, 'akagen')) // {username: 'akagen'}
console.log (removeUser(users, 'akagen')) // undefined