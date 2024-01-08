// Remove flash message after 3 seconds
setTimeout(function() {
    var flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
      message.style.opacity = '0';
      setTimeout(function() {
        message.remove();
      }, 300); // remove the message after the transition is complete
    });
  }, 3000); // 3000 milliseconds = 3 seconds