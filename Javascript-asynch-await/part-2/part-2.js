document.addEventListener('DOMContentLoaded', () => {
    let remainingCards = 52;
    let deckId = '';
    const cardsContainer = document.getElementById('cards');
    const cardWidth = 150;
    const cardHeight = 225;

    async function drawCard() {
        if (remainingCards === 0) {
            console.log("All cards have been drawn.");
            return;
        }

        try {
            const response = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=1`);
            const data = await response.json();
            const card = data.cards[0];
            console.log(`Card: ${card.value} of ${card.suit}`);
            remainingCards--;

            const cardDiv = document.createElement('div');
            cardDiv.classList.add('card');
            cardDiv.style.backgroundImage = `url(${card.image})`;

            const centerX = (cardsContainer.offsetWidth - cardWidth) / 16;
            const centerY = (cardsContainer.offsetHeight - cardHeight) / 4;

            const randomX = centerX + (Math.random() - 0.5) * cardWidth * 2;
            const randomY = centerY + (Math.random() - 0.5) * cardHeight * 2;
            const randomRotation = Math.random() * 360;

            cardDiv.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${randomRotation}deg)`;

            cardsContainer.appendChild(cardDiv);

            if (remainingCards === 0) {
                console.log("All cards have been drawn.");
            }
        } catch (error) {
            console.error(`Error drawing card: ${error}`);
        }
    }

    async function createNewDeck() {
        try {
            const response = await fetch('https://deckofcardsapi.com/api/deck/new/shuffle/');
            const data = await response.json();
            deckId = data.deck_id;
        } catch (error) {
            console.error(`Error creating deck: ${error}`);
        }
    }

    createNewDeck();

    const drawButton = document.getElementById('draw-button');
    drawButton.addEventListener('click', drawCard);
});
