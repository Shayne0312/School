document.addEventListener('DOMContentLoaded', function () {
    const savingForm = document.getElementById('savingForm');

    savingForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Fetch the form data
        const formData = new FormData(savingForm);

        // Make a POST request to the server with the form data
        fetch('/savings', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Check if the savings goal was added successfully
            if (data.success) {
                console.log('Savings goal added successfully!');
            } else {
                console.error('Failed to add savings goal.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function redirectToDashboard() {
    window.location.href = "{{ url_for('dashboard') }}";
}

function loadSavingsData() {
    const selectedDate = document.getElementById('selectSavingsDate').value;
    
    fetch('/load-savings-data')
        .then(response => response.json())
        .then(data => {
            console.log("Savings data loaded:", data);
            // Update the UI with the loaded savings data
            updateSavingsUI(data);
        })
        .catch(error => console.error('Error loading savings data:', error));
    }