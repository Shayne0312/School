document.addEventListener('DOMContentLoaded', () => {
    // Track the number of remaining cards
    let remainingCards = 52;
    // Variable to store the deck ID
    let deckId = '';
    // Container to display cards
    const cardsContainer = document.getElementById('cards');
    // Width of each card
    const cardWidth = 150;
    // Height of each card
    const cardHeight = 225;

    // Function to fetch a card from the deck
    function drawCard() {
        // Check if all cards have been drawn
        if (remainingCards === 0) {
            console.log("All cards have been drawn.");
            return;
        }

        // Fetch a card from the API
        fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=1`)
            .then(response => response.json())
            .then(data => {
                const card = data.cards[0];
                console.log(`Card: ${card.value} of ${card.suit}`);
                remainingCards--;

                // Create card element
                const cardDiv = document.createElement('div');
                cardDiv.classList.add('card');
                cardDiv.style.backgroundImage = `url(${card.image})`; // Use the card image provided by the API

                // Calculate center of the screen
                const centerX = (cardsContainer.offsetWidth - cardWidth) / 16;
                const centerY = (cardsContainer.offsetHeight - cardHeight) / 4;

                // Randomize position around the center
                const randomX = centerX + (Math.random() - 0.5) * cardWidth * 2; // Adjust spread as needed
                const randomY = centerY + (Math.random() - 0.5) * cardHeight * 2; // Adjust spread as needed
                const randomRotation = Math.random() * 360; // Random rotation between 0 and 360 degrees

                // Apply styles
                cardDiv.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${randomRotation}deg)`;

                // Append card to the container
                cardsContainer.appendChild(cardDiv);

                // Check if all cards have been drawn after this draw
                if (remainingCards === 0) {
                    console.log("All cards have been drawn.");
                }
            })
            .catch(error => console.error(`Error drawing card: ${error}`));
    }

    // Function to create a new shuffled deck
    function createNewDeck() {
        // Fetch a new shuffled deck from the API
        fetch('https://deckofcardsapi.com/api/deck/new/shuffle/')
            .then(response => response.json())
            .then(data => {
                // Store the deck ID
                deckId = data.deck_id;
            })
            .catch(error => console.error(`Error creating deck: ${error}`));
    }

    // Example usage: call createNewDeck() when the page loads
    createNewDeck();

    // Event listener for the draw button
    const drawButton = document.getElementById('draw-button');
    drawButton.addEventListener('click', drawCard);
});
