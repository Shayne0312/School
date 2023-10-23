"use strict";

// DOM elements
const $body = $("body");
const $storiesLoadingMsg = $("#stories-loading-msg");
const $allStoriesList = $("#all-stories-list");
const $favoritedStories = $("#favorited-stories");
const $ownStories = $("#my-stories");
const $storiesContainer = $("#stories-container");
const $storiesLists = $(".stories-list");
const $userProfile = $("#user-profile");
const $userProfileContainer = $("#user-profile-container");
const $accountFormsContainer = $("#account-forms-container");

// Forms
const $loginForm = $("#login-form");
const $signupForm = $("#signup-form");
const $submitForm = $("#submit-form");
const $editProfile = $("#edit-profile");
const $updateButton = $("#update-button");

// Navigation
const $navSubmitStory = $("#nav-submit-story");
const $navLogin = $("#nav-login");
const $navUserProfile = $("#nav-user-profile");
const $navLogOut = $("#nav-logout");

// Function to hide all page components 
function hidePageComponents() { 
  const components = [ 
    $storiesLists, 
    $submitForm, 
    $loginForm, 
    $signupForm, 
    $userProfile 
  ]; 
  components.forEach(component => component.hide()); 
} 

// Generate user profile
// Function to generate user profile 
function generateUserProfile() { 
  // Update user profile information 
  $("#profile-name").text(currentUser.name); 
  $("#profile-username").text(currentUser.username); 
  $("#profile-account-date").text(currentUser.createdAt.slice(0, 10)); 

   // Remove any existing edit profile form 
   $("#edit-profile").remove(); 

   // Create new edit profile form 
   const $updateProfileForm = $( ` 
     <form id="edit-profile"> 
       <h4>Update Profile</h4> 
       <div> 
         <label for="profile-edit-name">Name:</label> 
         <input id="profile-edit-name" type="text" value="${currentUser.name}" required> 
       </div> 
       <div> 
         <label for="profile-edit-password">Password:</label> 
         <input id="profile-edit-password" type="password" required> 
       </div> 
       <button type="submit">Update</button> 
     </form> 
   ` ); 

   // Add edit profile form to user profile section 
   $("#user-profile").append($updateProfileForm); 
 } 

// Start the application 
async function start() { 
  await checkForRememberedUser(); 
  await getAndShowStoriesOnStart(); 
  $accountFormsContainer.show(); 
  $storiesContainer.hide(); 
  $loginForm.show(); 
  $signupForm.show(); 

  // Update UI if user is logged in 
  if (currentUser) { 
    updateUIOnUserLogin(); 
    $loginForm.show(); 
    $signupForm.show(); 
  } 
  // Event listener for user profile button 
  $navUserProfile.on("click", showUserProfile); 
} 

// Event listener for all stories button 
$("#nav-all").on("click", showAllStories); 

// Show all stories
function showAllStories() { 
  hidePageComponents(); 
  $allStoriesList.show(); 
  $editProfile.hide(); 
} 

// Show user profile
function showUserProfile() { 
  hidePageComponents(); 
  $userProfile.show(); 
} 

// Start the application when DOM is ready
$(start);