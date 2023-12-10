function processForm(evt) {
    // Prevent default behavior
    evt.preventDefault();

    // Gather form data into JSON
    const formData = {
        name: $("#name").val(),
        year: $("#year").val(),
        email: $("#email").val(),
        color: $("#color").val()
    };

    // Make AJAX post request
    axios.post('/api/get-lucky-num', formData)
        .then(handleResponse)
        // catches any errors
        .catch(error => {
            // if an error is caught it parses the response
            if (error.response) {
                const errors = error.response.data.errors;
                for (const key in errors) {
                    // the the error is placed into the correct field
                    $(`#${key}-err`).text(errors[key]);
                }
            }
        });
}

// Handles response
function handleResponse(resp) {
    const data = resp.data;
    //  Interpolates the values into text data
    $('#lucky-results').text(`Your lucky number is ${data.num.num} (${data.num.fact}). Your birth year (${data.year.year}) fact is ${data.year.fact}.`);
}

// listens for submit event and calls process form
$("#lucky-form").on("submit", processForm);