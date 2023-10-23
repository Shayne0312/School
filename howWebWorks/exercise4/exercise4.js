
if (URL.canParse("../cats", "http://www.reddit.com/dogs")) {
    const url = new URL("../cats", "http://www.reddit.com/dogs");
    console.log(url.hostname); // "www.reddit.com"
    console.log(url.pathname); // "/cats"
} else {
    console.log("Invalid URL"); //Invalid URL
}

url.hash = "tabby";
console.log(url.href); // "http://www.reddit.com/cats#tabby"