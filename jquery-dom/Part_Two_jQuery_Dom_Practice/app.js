function createTable() {
    $("#table").append("<tbody id='table-body'></tbody>");

    $('#table').addClass("dynamicTable");
    $('#table thead').addClass("dynamicTableTh");
    $('#table tbody td').addClass("dynamicTableTd");
}

function addNewHeader(title, rating) {
    const removeButton = $("<button>")
        .text("Remove")
        .addClass("remove-button")
        .click(function() {
            $(this).closest("tr").remove();
        });

    const row = $("<tr>");
    row.append($("<td>").text(title).addClass("title-cell"));
    row.append($("<td>").append($("<span>").text(rating)).addClass("rating-cell"));
    row.append($("<td>").append(removeButton).addClass("remove-cell"));

    $("#table-body").append(row);
}

$(document).ready(function() {
    createTable();
    $("form").submit(function(event) {
        event.preventDefault();
        const title = $("#Title").val();
        const rating = $("#Rating").val();

        // Validate input values
        if (title.length < 2) {
            $("#titleError").text("Title must have at least 2 characters.");
            return;
        } else {
            $("#titleError").text("");
        }

        if (rating < 0 || rating > 10) {
            $("#ratingError").text("Rating must be between 0 and 10.");
            return;
        } else {
            $("#ratingError").text("");
        }

        addNewHeader(title, rating);
        $("form")[0].reset();
    });
});

function addNewHeader(title, rating) {
    const removeButton = $("<button>")
        .text("Remove")
        .addClass("remove-button")
        .click(function() {
            $(this).closest("tr").remove();
        });

    const row = $("<tr>");
    row.append($("<td>").text(title).addClass("title-cell"));
    row.append($("<td>").text(rating).addClass("rating-cell"));
    row.append($("<td>").append(removeButton).addClass("remove-cell"));

    $("#table-body").append(row);
}
