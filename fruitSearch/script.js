const input = document.querySelector('#fruit');
const suggestions = document.querySelector('.suggestions ul');

const fruit = ['Apple', 'Apricot', 'Avocado 🥑', 'Banana', 'Bilberry', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Boysenberry', 'Currant', 'Cherry', 'Coconut', 'Cranberry', 'Cucumber', 'Custard apple', 'Damson', 'Date', 'Dragonfruit', 'Durian', 'Elderberry', 'Feijoa', 'Fig', 'Gooseberry', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Honeyberry', 'Huckleberry', 'Jabuticaba', 'Jackfruit', 'Jambul', 'Juniper berry', 'Kiwifruit', 'Kumquat', 'Lemon', 'Lime', 'Loquat', 'Longan', 'Lychee', 'Mango', 'Mangosteen', 'Marionberry', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Miracle fruit', 'Mulberry', 'Nectarine', 'Nance', 'Olive', 'Orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Pineapple', 'Pomegranate', 'Pomelo', 'Quince', 'Raspberry', 'Salmonberry', 'Rambutan', 'Redcurrant', 'Salak', 'Satsuma', 'Soursop', 'Star fruit', 'Strawberry', 'Tamarillo', 'Tamarind', 'Yuzu'];

function search(str, fruit) {
  const results = [];
  for (const item of fruit) {
    if (item.toLowerCase().startsWith(str.toLowerCase())) {
      results.push(item);
      if (results.length === 3) break;
    }
  }
  return results;
}

function searchHandler(e) {
	const inputVal = e.target.value;
	if (inputVal === "") {
	  input.placeholder = "Search fruit 🍎";
	  suggestions.parentNode.style.display = 'none';
	} else {
	  const results = search(inputVal, fruit);
	  showSuggestions(results);
	}
  }

function showSuggestions(results) {
  if (results.length > 0) {
    suggestions.innerHTML = results.map(result => `<li>${result}</li>`).join('');
    suggestions.parentNode.style.display = 'block';
  } else {
    suggestions.parentNode.style.display = 'none';
  }
}

function useSuggestion(e) {
  if (e.target.tagName === 'LI') {
    input.value = e.target.textContent;
    suggestions.parentNode.style.display = 'none';
  }
}

input.addEventListener('input', searchHandler);
suggestions.addEventListener('click', useSuggestion);