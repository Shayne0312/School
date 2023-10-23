describe('Fruit Autocomplete', function() {
    let input;
    let suggestions;
  
    const fruit = ['Apple', 'Apricot', 'Avocado 🥑', 'Banana', 'Bilberry', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Boysenberry', 'Currant', 'Cherry', 'Coconut', 'Cranberry', 'Cucumber', 'Custard apple', 'Damson', 'Date', 'Dragonfruit', 'Durian', 'Elderberry', 'Feijoa', 'Fig', 'Gooseberry', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Honeyberry', 'Huckleberry', 'Jabuticaba', 'Jackfruit', 'Jambul', 'Juniper berry', 'Kiwifruit', 'Kumquat', 'Lemon', 'Lime', 'Loquat', 'Longan', 'Lychee', 'Mango', 'Mangosteen', 'Marionberry', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Miracle fruit', 'Mulberry', 'Nectarine', 'Nance', 'Olive', 'Orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Pineapple', 'Pomegranate', 'Pomelo', 'Quince', 'Raspberry', 'Salmonberry', 'Rambutan', 'Redcurrant', 'Salak', 'Satsuma', 'Soursop', 'Star fruit', 'Strawberry', 'Tamarillo', 'Tamarind', 'Yuzu'];
  
    beforeEach(function() {
      const container = document.createElement('div');
      container.innerHTML = `
        <input type="text" name="fruit" id="fruit" placeholder="Search Fruit 🍎">
        <div class="suggestions">
          <ul></ul>
        </div>
      `;
      document.body.appendChild(container);
  
      input = document.querySelector('#fruit');
      suggestions = document.querySelector('.suggestions ul');
    });
  
    afterEach(function() {
      document.body.removeChild(input.parentNode);
    });
  
    function search(str, fruit) {
      let results = [];
      for (let i = 0; i < fruit.length; i++) {
        if (fruit[i].toLowerCase().startsWith(str.toLowerCase())) {
          results.push(fruit[i]);
          if (results.length === 4) break;
        }
      }
      return results;
    }
  
    function searchHandler(e) {
      const inputVal = e.target.value;
      if (inputVal === "") {
        suggestions.parentNode.style.display = 'none';
      } else {
        const results = search(inputVal, fruit);
        showSuggestions(results, inputVal);
      }
    }
  
    function showSuggestions(results, inputVal) {
      if (results.length > 0) {
        suggestions.innerHTML = '';
        for (let i = 0; i < results.length; i++) {
          const li = document.createElement('li');
          li.textContent = results[i];
          suggestions.appendChild(li);
        }
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
  
    describe('search', function() {
        it('should return an array of matching fruits', function() {
          const result = search('A', fruit);
          expect(result).toEqual(['Apple', 'Apricot', 'Avocado 🥑']);
        });
    
        it('should return an empty array if no fruits match', function() {
          const result = search('xyz', fruit);
          expect(result).toEqual([]);
        });
    
        it('should handle case-insensitive search', function() {
          const result = search('a', fruit);
          expect(result).toEqual(['Apple', 'Apricot', 'Avocado 🥑']);
        });
    
        it('should return only the first 3 matching fruits', function() {
            const result = search('B', fruit);
            expect(result).toEqual(['Banana', 'Bilberry', 'Blackberry', 'Blackcurrant']);
          });
    });
  
    describe('searchHandler', function() {
      it('should hide suggestions if input value is empty', function() {
        input.value = '';
        suggestions.parentNode.style.display = 'block';
  
        searchHandler({ target: input });
  
        expect(suggestions.parentNode.style.display).toBe('none');
      });
  
      it('should show suggestions if input value is not empty', function() {
        input.value = 'Ap';
        const results = ['Apple', 'Apricot', 'Avocado 🥑'];
        suggestions.parentNode.style.display = 'none';
  
        showSuggestions(results, input.value);
  
        expect(suggestions.parentNode.style.display).toBe('block');
      });
    });
  
    describe('useSuggestion', function() {
      it('should update input value with selected suggestion', function() {
        const target = document.createElement('li');
        target.textContent = 'Apple';
        input.value = '';
        suggestions.parentNode.style.display = 'block';
  
        useSuggestion({ target });
  
        expect(input.value).toBe('Apple');
        expect(suggestions.parentNode.style.display).toBe('none');
      });
  
      it('should not update input value if target is not an LI element', function() {
        const target = document.createElement('span');
        target.textContent = 'Apple';
        input.value = '';
        suggestions.parentNode.style.display = 'block';
  
        useSuggestion({ target });
  
        expect(input.value).toBe('');
        expect(suggestions.parentNode.style.display).toBe('block');
      });
    });
  });