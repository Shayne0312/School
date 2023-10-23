// ES5 global constants
var PI = 3.14;
PI = 42; // stop me from doing this!

// ES2015 Global Constants
const PI = 3.14;
PI = 42; // This will throw an error

// What is the difference between var and let?
    
// You can reassign and redeclare with var, but you can not redeclare using the let keyword. You can access a hoisted variable with var. Let creates block scope.
    
// What is the difference between var and const?
    
// You can reassign and redeclare with var, but you can not redeclare or reassign using the const keyword. You can access a hoisted variable with var. Const creates block scope.
    
// What is the difference between let and const?
    
// You can reassign with let, but you can not redeclare or reassign using the const keyword.
    
// What is hoisting?
    
// It’s the way that we explain how the JS compiler works. Variables are lifting or “hoisted” to the top of the scope they are declared in. When using var, you can access the variable name and it’s undefined value before it is used later on.
    
// Function declarations are also hoisted and can be invoked “before” they are defined in a codebase.