// Constants
const NUM_CATEGORIES = 6;
const NUM_QUESTIONS_PER_CAT = 5;

// Jeopardy board element
const jeopardyBoard = $("#jeopardy");

// Array to store category data
const categories = [];

// Function to get random category IDs
function getCategoryIds(catIds) {
  // Get random category IDs from the provided data
  const randomIds = _.sampleSize(catIds.data, NUM_CATEGORIES);
  // Extract only the IDs from the random category data
  const categoryIds = randomIds.map(cat => cat.id);
  return categoryIds;
}

// Function to get category data
function getCategory(catId) {
  // Get the category data for the provided ID
  const cat = catId.data;
  // Get random clues from the category data
  const clues = _.sampleSize(cat, NUM_QUESTIONS_PER_CAT);
  // Create an object with the category title and the clues
  const catData = {
    title: cat[0].category.title,
    clues: clues.map(arr => ({
      question: arr.question,
      answer: arr.answer,
      showing: null
    }))
  };
  // Add the category data to the categories array
  categories.push(catData);
}

// Function to fill the jeopardy table
function fillTable() {
  // Get the titles of the categories
  const titles = categories.map(title => title.title);
  // Get the table header element
  const thead = $("thead");
  // Create table headers for each category
  for (let x = 0; x < NUM_CATEGORIES; x++) {
    const catHeader = document.createElement("th");
    catHeader.innerText = titles[x];
    thead.append(catHeader);
  }
  // Create table cells for each clue
  for (let y = 0; y < NUM_QUESTIONS_PER_CAT; y++) {
    const row = document.createElement("tr");
    for (let x = 0; x < NUM_CATEGORIES; x++) {
      const cell = document.createElement("td");
      cell.innerHTML = `<div id="${x}-${y}">?</div>`;
      row.append(cell);
    }
    jeopardyBoard.append(row);
  }
}

// Function to handle click events
function handleClick(e) {
  const x = e.target.id[0];
  const y = e.target.id[2];
  if (e.target.classList.contains("answer")) {
    return;
  } else if (e.target.classList.contains("question")) {
    e.target.innerText = categories[x].clues[y].answer;
    e.target.classList.remove("question");
    e.target.classList.add("answer");
  } else {
    e.target.innerText = categories[x].clues[y].question;
    e.target.classList.add("question");
  }
}

// Function to setup and start the game
async function setupAndStart() {
  try {
    // Get random categories from the API
    const resCategories = await axios.get("http://jservice.io/api/categories", {
      params: {
        count: 100
      }
    });
    // Get random category IDs
    const catIds = getCategoryIds(resCategories);
    // Get category data for each ID
    for (const id of catIds) {
      const resTitles = await axios.get("http://jservice.io/api/clues", {
        params: {
          category: id
        }
      });
      getCategory(resTitles);
    }
    // Fill the jeopardy table with the category data
    fillTable();
  } catch (error) {
    console.error("Error:", error);
  }
}

// Event listener for restart button
$("#restart").on("click", function() {
  location.reload();
});

// Setup and start the game when the document is ready
$(document).ready(function() {
  setupAndStart();
  jeopardyBoard.on("click", "div", handleClick);
});