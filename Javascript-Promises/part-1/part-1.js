// Part 1: Number Facts
function getFact(number) {
    return fetch(`http://numbersapi.com/${number}?json`)
      .then(response => response.json())
      .then(data => data.text);
  }
  
  function getMultipleFacts(numbers) {
    const promises = numbers.map(number => getFact(number));
    return Promise.all(promises).then(facts => facts.join('\n'));
  }
  
  const favoriteNumber = 42;
  
  getFact(favoriteNumber)
    .then(fact => {
      console.log(`Fact about ${favoriteNumber}: ${fact}`);
      document.getElementById('number-fact').textContent = fact;
    })
    .catch(error => console.error(`Error fetching fact: ${error}`));
  
  getMultipleFacts([1, 3, 7, 11])
    .then(facts => {
      console.log(`Multiple facts:\n${facts}`);
      document.getElementById('multiple-facts').textContent = facts;
    })
    .catch(error => console.error(`Error fetching multiple facts: ${error}`));