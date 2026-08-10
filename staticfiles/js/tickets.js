document.addEventListener("DOMContentLoaded", function () {
    const saveCloseBtn = document.getElementById("saveCloseBtn");

    if (saveCloseBtn) {
        saveCloseBtn.addEventListener("click", function () {
            // Future: AJAX save or form submit
            window.close();
        });
    }
});
