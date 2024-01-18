function confirmDelete() {
    if (confirm("Are you sure you want to delete your account?")) {
        document.getElementById('delete-account-form').submit();
    } else {
        // Prevent form submission if the user clicks "cancel"
        event.preventDefault();
    }
}