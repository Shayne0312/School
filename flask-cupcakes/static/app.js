$(document).ready(function() {
    // Function to get cupcakes from the API and update the cupcake list
    function getCupcakes() {
        axios.get('/api/cupcakes')
            .then(function(response) {
                const cupcakes = response.data.cupcakes;
                const cupcakeList = $('#cupcake-list');
                cupcakeList.empty();

                for (const cupcake of cupcakes) {
                    const listItem = $('<li>').text(`Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}`);
                    const image = $('<img>').attr('src', cupcake.image).attr('alt', cupcake.flavor);
                    listItem.append(image);
                    cupcakeList.append(listItem);
                }
            })
            .catch(function(error) {
                console.log(error);
            });
    }

    // Function to handle form submission and add a new cupcake
    $('#cupcake-form').submit(function(event) {
        event.preventDefault();

        const flavor = $('#flavor-input').val();
        const size = $('#size-input').val();
        const rating = $('#rating-input').val();
        const image = $('#image-input').val();

        const cupcakeData = {
            flavor: flavor,
            size: size,
            rating: rating,
            image: image
        };

        axios.post('/api/cupcakes', cupcakeData)
            .then(function(response) {
                getCupcakes();
                $('#flavor-input').val('');
                $('#size-input').val('');
                $('#rating-input').val('');
                $('#image-input').val('');
            })
            .catch(function(error) {
                console.log(error);
            });
    });

    // Initial call to get cupcakes and update the cupcake list
    getCupcakes();
});