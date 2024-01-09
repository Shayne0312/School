"use strict";

// Global variables
let currentUser;

// Function to handle login event
async function handleLoginEvent(evt) {
  evt.preventDefault();

  // Get username and password from input fields
  const username = $("#login-username").val();
  const password = $("#login-password").val();

  // Login user and store the current user
  currentUser = await User.login(username, password);

  // Reset login form
  $loginForm.trigger("reset");

  // Save user credentials in local storage
  saveUserCredentialsInLocalStorage();

  // Update UI on user login
  updateUIOnUserLogin();
}

// Event listener for login form submission
$loginForm.on("submit", handleLoginEvent);

// Function to handle signup event
async function handleSignupEvent(evt) {
  evt.preventDefault();

  // Get name, username, and password from input fields
  const name = $("#signup-name").val();
  const username = $("#signup-username").val();
  const password = $("#signup-password").val();

  // Sign up user and store the current user
  currentUser = await User.signup(username, password, name);

  // Save user credentials in local storage
  saveUserCredentialsInLocalStorage();

  // Update UI on user login
  updateUIOnUserLogin();

  // Reset signup form
  $signupForm.trigger("reset");
}

// Event listener for signup form submission
$signupForm.on("submit", handleSignupEvent);

// Function to handle logout event
function handleLogoutEvent(evt) {
  // Clear local storage
  localStorage.clear();

  // Reload the page
  location.reload();
}

// Event listener for logout button click
$navLogOut.on("click", handleLogoutEvent);

// Function to check if there is a remembered user in local storage
async function checkForRememberedUser() {
  // Get token and username from local storage
  let token = localStorage.getItem("token");
  let username = localStorage.getItem("username");

  // If token or username is missing, return false
  if (!token || !username) {
    return false;
  }

  // Login user via stored credentials and store the current user
  currentUser = await User.loginViaStoredCredentials(token, username);

  // If the loginViaStoredCredentials function returns null, the credentials are invalid
  if (!currentUser) {
    // Clear the invalid credentials from local storage
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    return false;
  }

  // If the credentials are valid, check if they have been updated
  const updatedToken = localStorage.getItem("token");
  const updatedUsername = localStorage.getItem("username");

  if (updatedToken !== token || updatedUsername !== username) {
    // Update the token and username in local storage
    token = updatedToken;
    username = updatedUsername;
  }

  return true;
}

// Function to update user profile information displayed on the page
function updateUserProfile() {
  $("#profile-name").text(currentUser.name);
  $("#profile-username").text(currentUser.username);
  $("#profile-account-date").text(currentUser.createdAt.slice(0, 10));
  $("#nav-user-profile").text(currentUser.username);
}

// Function to handle profile update event
async function handleProfileUpdateEvent(evt) {
  evt.preventDefault();

  const username = $("#profile-edit-name").val();
  const password = $("#profile-edit-password").val();

  const updatedUser = await currentUser.updateUser(username, password);

  // Update current user
  currentUser = updatedUser;

  // Update user profile information displayed on the page
  updateUserProfile();
}

// Event listener for profile update form submission
$body.on("submit", "#edit-profile", handleProfileUpdateEvent);

// Function to save user credentials in local storage
function saveUserCredentialsInLocalStorage() {
  if (currentUser) {
    localStorage.setItem("token", currentUser.loginToken);
    localStorage.setItem("username", currentUser.username);
  }
}

// Function to update UI on user login
async function updateUIOnUserLogin() {
  // Hide page components
  hidePageComponents();

  // Put stories on the page
  putStoriesOnPage();

  // Show all stories list
  $allStoriesList.show();

  // Update navigation on login
  updateNavOnLogin();

  // Generate user profile
  generateUserProfile();

  // Show stories container
  $storiesContainer.show();
}

// Function to generate user profile
function generateUserProfile() {
  // Set user profile information
  $("#profile-name").text(currentUser.name);
  $("#profile-username").text(currentUser.username);
  $("#profile-account-date").text(currentUser.createdAt.slice(0, 10));
}