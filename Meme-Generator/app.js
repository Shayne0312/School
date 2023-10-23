// Get form and image container elements
const form = document.getElementById('meme-form');
const imgContainer = document.querySelector('.imgContainer');

// Event listener for form submission
form.addEventListener('submit', function(e) {
  e.preventDefault();

  // Get input values
  const topText = document.getElementById('top-text').value;
  const bottomText = document.getElementById('bottom-text').value;
  const imageUrl = document.getElementById('image-url').value;

  // Check if all inputs are filled
  if (topText && bottomText && imageUrl) {
    // Check if maximum number of images is reached
    if (imgContainer.childElementCount < 4) {
      // Create meme element
      const meme = createMemeElement(topText, bottomText, imageUrl);
      // Append meme to image container
      imgContainer.appendChild(meme);
      // Reset form inputs
      form.reset();
    } else {
      alert('Maximum of 4 images allowed.');
    }
  }
});

// Function to create a meme element
function createMemeElement(topText, bottomText, imageUrl) {
  const meme = document.createElement('div');
  meme.classList.add('img');

  // Create top text element
  const topTextDisplay = document.createElement('p');
  topTextDisplay.classList.add('top-text');
  topTextDisplay.innerText = topText;
  topTextDisplay.style.fontSize = `${document.getElementById('text-size').value}px`;
  topTextDisplay.style.transform = `rotate(${document.getElementById('text-rotation').value}deg)`;

  // Create bottom text element
  const bottomTextDisplay = document.createElement('p');
  bottomTextDisplay.classList.add('bottom-text');
  bottomTextDisplay.innerText = bottomText;
  bottomTextDisplay.style.fontSize = `${document.getElementById('text-size').value}px`;
  bottomTextDisplay.style.transform = `rotate(${document.getElementById('text-rotation').value}deg)`;

  // Create image element
  const img = document.createElement('img');
  img.src = imageUrl;

  // Create delete button element
  const deleteButton = document.createElement('button');
  deleteButton.classList.add('deleteButton');
  deleteButton.innerText = 'X';

  // Event listener for delete button click within a meme
  deleteButton.addEventListener('click', function(e) {
    // Remove the parent meme element
    e.target.parentNode.remove();
  });

  // Append elements to meme
  meme.appendChild(topTextDisplay);
  meme.appendChild(img);
  meme.appendChild(bottomTextDisplay);
  meme.appendChild(deleteButton);

  // Update meme text color
  meme.style.color = document.getElementById('text-color').value;

  return meme;
}