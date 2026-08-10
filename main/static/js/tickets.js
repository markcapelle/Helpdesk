document.addEventListener("DOMContentLoaded", function () {
    const saveCloseBtn = document.getElementById("saveCloseBtn");
    const form = document.querySelector("form");

    if (saveCloseBtn && form) {
        saveCloseBtn.addEventListener("click", async function () {

            const formData = new FormData(form);

            // Add a flag so Django knows this is Save & Close
            formData.append("save_and_close", "1");

            const response = await fetch(window.location.href, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            // After Django saves, close the tab
            window.close();
        });
    }
});