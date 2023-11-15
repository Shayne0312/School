// Add event listener to the new user form submission
document.getElementById("newUserForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submission

  // Perform the create request using fetch API
  fetch('/', {
    method: 'POST',
    body: new FormData(this)
  })
  .then(response => {
    if (response.ok) {
      // User created successfully
      alert("User created successfully!");
      window.location.href = "/users"; // Redirect to users list
    } else {
      // Failed to create user
      alert("Failed to create user");
    }
  })
  .catch(error => {
    // Error occurred while creating the user
    console.error(error);
    alert("An error occurred while creating the user");
  });
});