"use strict";

// Initialize variables
let storyList;

// Get all stories and show them on page load
async function getAndShowStoriesOnStart() {
  try {
    storyList = await StoryList.getStories();
    $storiesLoadingMsg.remove();
  } catch (error) {
    console.error("Error getting stories:", error);
  }
}

// Generate the HTML markup for a story
function generateStoryMarkup(story, showDeleteBtn = false) {
  const hostName = story.getHostName();
  const showStar = Boolean(currentUser);
  return $( `
    <li id="${story.storyId}">
      <div>
        ${showDeleteBtn ? getDeleteBtnHTML() : ""}
        ${showStar ? getStarHTML(story, currentUser) : ""}
        <a href="${story.url}" target="_blank" class="story-link">
          ${story.title}
        </a>
        <small class="story-hostname">(${hostName})</small>
        <div class="story-author">by ${story.author}</div>
        <div class="story-user">posted by ${story.username}</div>
      </div>
    </li>
  ` );
}

// Generate the HTML markup for the delete button
function getDeleteBtnHTML() {
  return  `
    <span class="trash-can">
      <i class="fas fa-trash-alt"></i>
    </span>` ;
}

// Generate the HTML markup for the star button
function getStarHTML(story, user) {
  const isFavorite = user.isFavorite(story);
  const starType = isFavorite ? "fas" : "far";
  return  `
    <span class="star">
      <i class="${starType} fa-star"></i>
    </span>` ;
}

// Put all the stories on the page
async function putStoriesOnPage() {
  try {
    $allStoriesList.empty();
    $storiesLoadingMsg.show();
    storyList.stories.forEach((story) => {
      const $story = generateStoryMarkup(story);
      $allStoriesList.append($story);
    });
    $storiesLoadingMsg.hide();
  } catch (error) {
    console.error("Error putting stories on page:", error);
  }
}

// Delete a story from the list
async function deleteStory(evt) {
  try {
    const $closestLi = $(evt.target).closest("li");
    const storyId = $closestLi.attr("id");
    await storyList.removeStory(currentUser, storyId);
    await putUserStoriesOnPage();
  } catch (error) {
    console.error("Error deleting story:", error);
  }
}

// Add a new story to the list
async function submitNewStory(evt) {
  try {
    evt.preventDefault();
    const title = $("#create-title").val();
    const url = $("#create-url").val();
    const author = $("#create-author").val();
    const username = currentUser.username;
    const storyData = { title, url, author, username };
    const story = await storyList.addStory(currentUser, storyData);
    const $story = generateStoryMarkup(story);
    $allStoriesList.prepend($story);
    $submitForm.slideUp("slow");
    $submitForm.trigger("reset");
  } catch (error) {
    console.error("Error submitting new story:", error);
  }
}

// Put the user's stories on the page
function putUserStoriesOnPage() {
  try {
    $ownStories.empty();
    if (currentUser.ownStories.length === 0) {
      $ownStories.append("<h5>No stories added by user yet!</h5>");
    } else {
      for (let story of currentUser.ownStories) {
        let $story = generateStoryMarkup(story, true);
        $ownStories.append($story);
      }
    }
    $ownStories.show();
  } catch (error) {
    console.error("Error putting user stories on page:", error);
  }
}

// Put the user's favorite stories on the page
function putFavoritesListOnPage() {
  try {
    $favoritedStories.empty();
    if (currentUser.favorites.length === 0) {
      $favoritedStories.append("<h5>No favorites added!</h5>");
    } else {
      for (let story of currentUser.favorites) {
        const $story = generateStoryMarkup(story);
        $favoritedStories.append($story);
      }
    }
    $favoritedStories.show();
  } catch (error) {
    console.error("Error putting favorites on page:", error);
  }
}

// Toggle a story's favorite status
async function toggleStoryFavorite(evt) {
  try {
    const $tgt = $(evt.target);
    const $closestLi = $tgt.closest("li");
    const storyId = $closestLi.attr("id");
    const story = storyList.stories.find((s) => s.storyId === storyId);
    if ($tgt.hasClass("fas")) {
      await currentUser.removeFavorite(story);
      $tgt.closest("i").toggleClass("fas far");
    } else {
      await currentUser.addFavorite(story);
      $tgt.closest("i").toggleClass("fas far");
    }
  } catch (error) {
    console.error("Error toggling story favorite:", error);
  }
}

// Set up event listeners
$(window).on("scroll", function () {
  if ($(window).scrollTop() + $(window).height() >= $(document).height()) {
    putStoriesOnPage();
  }
});

$ownStories.on("click", ".trash-can", deleteStory);
$submitForm.on("submit", submitNewStory);
$storiesLists.on("click", ".star", toggleStoryFavorite);