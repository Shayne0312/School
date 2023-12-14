// app.js

// Fetch company data from API
fetch(`https://cloud.iexapis.com/stable/stock/aapl/company?token=pk_e720ab208e4840d68ac8b89132bef85b`)
  .then(response => response.json())
  .then(data => {

    // Get reference to container element
    const container = document.getElementById('companies');

    // Loop through data and create card for each company
    data.forEach(company => {
    
      // Create elements
      const card = document.createElement('div');
      const name = document.createElement('h3');
      const description = document.createElement('p');

      // Add content
      name.textContent = company.name;
      description.textContent = company.description;

      // Add styling  
      card.className = 'card';

      // Append elements
      card.appendChild(name);
      card.appendChild(description);
      container.appendChild(card);

    });

});