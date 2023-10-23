// Function to search and display GIFs from Giphy API
async function searchAndDisplayGifs(searchTerm) {
    const API_KEY = 'fnRHMIsKMmtBnjL2WvAbT2uYq2i5g0TD';
    const API_URL = `http://api.giphy.com/v1/gifs/search?q=${searchTerm}&api_key=${API_KEY}`;
  
    // Retrieves GIF data from the API and display the next image in the gifContainer
    // and sends a GET request to the API URL, then extracs GIF data from the response.
    // lastly, it creates an img element and appends it to the gifContainer.
    try {
        const response = await axios.get(API_URL);
        const gifData = response.data.data;
        const gifContainer = document.getElementById('gifContainer');

        // If the gifContainer is empty, display the first image
        // Otherwise, display the next image
        // If there are no more images to display, do nothing
        const nextImageIndex = gifContainer.childElementCount;
        if (nextImageIndex < gifData.length) {
          const gif = gifData[nextImageIndex];
          const gifUrl = gif.images.fixed_height.url;
          const img = document.createElement('img');
          img.setAttribute('src', gifUrl);
          gifContainer.appendChild(img);
        }
      } catch (error) {
        // Handles any errors
        if (error.response) {
            alert('Error making request to Giphy API');
        console.error('Error searching and displaying GIFs:', error);
      }
    }
    }
  
    // Event listener for form submission
  document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const search = document.getElementById('search').value;
    searchAndDisplayGifs(search);
  });
  
    // Event listener for reset button
    document.getElementById('searchForm').addEventListener('reset', function() {
        const gifContainer = document.getElementById('gifContainer');
        gifContainer.innerHTML = '';
      });

  // Variable to keep track of the flicker animation state
let animationState = false;

// Function to start or stop the flicker animation
function toggleFlickerAnimation() {
  const neonText = document.querySelector('.neonText');
  if (animationState) {
    neonText.style.animation = 'none';
  } else {
    neonText.style.animation = 'flicker 1.5s infinite alternate';
  }
  animationState = !animationState;
}

// Event listener for NeonIO button click
document.getElementById('neonIO').addEventListener('click', toggleFlickerAnimation);
