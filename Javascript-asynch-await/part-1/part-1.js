async function getFact(number) {
  const response = await fetch(`http://numbersapi.com/${number}?json`);
  const data = await response.json();
  return data.text;
}

async function getMultipleFacts(numbers) {
  const promises = numbers.map(async (number) => await getFact(number));
  const facts = await Promise.all(promises);
  return facts.join('\n');
}

const favoriteNumber = 42;

(async () => {
  try {
    const fact = await getFact(favoriteNumber);
    console.log(`Fact about ${favoriteNumber}: ${fact}`);
    document.getElementById('number-fact').textContent = fact;
  } catch (error) {
    console.error(`Error fetching fact: ${error}`);
  }
})();

(async () => {
  try {
    const facts = await getMultipleFacts([1, 3, 7, 11]);
    console.log(`Multiple facts:\n${facts}`);
    document.getElementById('multiple-facts').textContent = facts;
  } catch (error) {
    console.error(`Error fetching multiple facts: ${error}`);
  }
})();
