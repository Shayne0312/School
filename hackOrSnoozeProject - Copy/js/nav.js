"use strict";

// Show main list of all stories when clicking site name
function navAllStories(evt) {
  hidePageComponents();
  $storiesContainer.show();
  $allStoriesList.show();
  $userProfile.hide();
  $userProfileContainer.hide();
}
$body.on("click", "#nav-all", navAllStories);

// Show story submit form when clicking "submit"
function navSubmitStoryClick(evt) {
  hidePageComponents();
  $storiesContainer.show();
  $allStoriesList.show();
  $submitForm.show();
  $userProfileContainer.hide();
}
$navSubmitStory.on("click", navSubmitStoryClick);

// Show favorite stories when clicking "favorites"
function navFavoritesClick(evt) {
  hidePageComponents();
  putFavoritesListOnPage();
  $favoritedStories.show();
  $storiesContainer.show();
  $editProfile.hide();
  $userProfileContainer.hide();
}
$body.on("click", "#nav-favorites", navFavoritesClick);

// Show My Stories when clicking "my stories"
function navMyStories(evt) {
  hidePageComponents();
  putUserStoriesOnPage();
  $ownStories.show();
  $storiesContainer.show();
  $editProfile.hide();
  $userProfileContainer.hide();
}
$body.on("click", "#nav-my-stories", navMyStories);

// Show login/signup when clicking "login"
function navLoginClick(evt) {
  hidePageComponents();
  $loginForm.show();
  $signupForm.show();
  $storiesContainer.hide();
}
$navLogin.on("click", navLoginClick);

// Show user profile when clicking "profile" in the navigation bar
function navProfileClick(evt) {
  hidePageComponents();
  generateUserProfile();
  $storiesContainer.hide();
  $allStoriesList.hide();
  $userProfile.show();
  $userProfileContainer.show();
  $editProfile.show();
}
$navUserProfile.on("click", navProfileClick);

// Show main list of all stories when clicking "update profile"
function navProfileUpdateClick(evt) {
  hidePageComponents();
  $storiesContainer.show();
  $allStoriesList.show();
  $userProfile.hide();
  $userProfileContainer.hide();
}
$updateButton.on("click", navProfileUpdateClick);

// Update the navbar to reflect that a user is logged in
function updateNavOnLogin() {
  $(".main-nav-links").css("display", "flex");
  $navLogin.hide();
  $navLogOut.show();
  $navUserProfile.text( `${currentUser.username}` ).show();
}